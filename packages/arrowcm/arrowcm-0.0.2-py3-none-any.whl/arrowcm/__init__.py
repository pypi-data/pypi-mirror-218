import mimetypes
import os
from base64 import decodebytes, encodebytes
from datetime import datetime
from typing import Any, Type

import nbformat
from jupyter_server.services.contents.checkpoints import Checkpoints
from jupyter_server.services.contents.filecheckpoints import GenericFileCheckpoints
from jupyter_server.services.contents.manager import ContentsManager
from pyarrow import fs
from tornado import web
from tornado.web import HTTPError
from traitlets import Instance

EPOCH = datetime.fromtimestamp(0)

MODEL_TYPE_DIRECTORY = "directory"
MODEL_TYPE_FILE = "file"
MODEL_TYPE_NOTEBOOK = "notebook"
NOTEBOOK_EXTENSION = ".ipynb"


class ArrowContentsManager(ContentsManager):
    filesystem = Instance(fs.FileSystem, config=True)

    def _base_model(self, fi: fs.FileInfo, path: str) -> dict[str, Any]:
        four_o_four = "file or directory does not exist: %r" % path

        if not self.allow_hidden and self.is_hidden(path):
            self.log.info("Refusing to serve hidden file or directory %r, via 404 Error", path)
            raise web.HTTPError(404, four_o_four)

        if isinstance(fi.mtime, float):
            last_modified = tz.utcfromtimestamp(fi.mtime)
        else:
            last_modified = fi.mtime or EPOCH

        model = {}
        model["name"] = path.rsplit("/", 1)[-1]
        model["path"] = path
        model["last_modified"] = last_modified
        model["created"] = last_modified
        model["content"] = None
        model["format"] = None
        model["mimetype"] = None
        model["size"] = fi.size
        model["writable"] = True

        return model

    def _dir_model(self, fi: fs.FileInfo, path: str, content: bool = True) -> dict[str, Any]:
        """Build a model for a directory

        if content is requested, will include a listing of the directory
        """
        model = self._base_model(fi, path)

        four_o_four = "directory does not exist: %r" % path

        if fi.type is not fs.FileType.Directory:
            raise web.HTTPError(404, four_o_four)
        elif not self.allow_hidden and self.is_hidden(path):
            self.log.info("Refusing to serve hidden directory %r, via 404 Error", os_path)
            raise web.HTTPError(404, four_o_four)

        model["type"] = MODEL_TYPE_DIRECTORY
        model["size"] = None
        if content:
            model["content"] = contents = []
            selector = fs.FileSelector(fi.path, recursive=False)
            for child in self.filesystem.get_file_info(selector):
                if self.should_list(child.base_name) and (self.allow_hidden or not self.is_hidden(child.path)):
                    child_model = self.get(path=f"{path}/{child.base_name}", content=False, fi=child)
                    contents.append(child_model)

            model["format"] = "json"

        return model

    def _file_model(
        self,
        fi: fs.FileInfo,
        path: str,
        content: bool = True,
        format: str | None = None,
    ) -> dict[str, Any]:
        """Build a model for a file

        if content is requested, include the file contents.

        format:
          If 'text', the contents will be decoded as UTF-8.
          If 'base64', the raw bytes contents will be encoded as base64.
          If not specified, try to decode as UTF-8, and fall back to base64
        """
        model = self._base_model(fi, path)
        model["type"] = MODEL_TYPE_FILE
        model["mimetype"] = mimetypes.guess_type(fi.base_name)[0]

        if content:
            with self.filesystem.open_input_file(fi.path) as fp:
                bcontent = fp.readall()
                try:
                    model["content"] = bcontent.decode("utf8")
                    model["format"] = "text"
                except UnicodeError as exc:
                    if format == "text":
                        raise HTTPError(
                            400,
                            f"{path} is not UTF-8 encoded",
                            reason="bad format",
                        ) from exc
                    else:
                        model["content"] = encodebytes(bcontent).decode("ascii")
                        model["format"] = "base64"

            if model["mimetype"] is None:
                model["mimetype"] = "text/plain" if format == "text" else "application/octet-stream"

        return model

    def _notebook_model(self, fi: fs.FileInfo, path: str, content: bool = True) -> dict[str, Any]:
        """Build a notebook model

        if content is requested, the notebook content will be populated
        as a JSON structure (not double-serialized)
        """
        model = self._base_model(fi, path)
        model["type"] = MODEL_TYPE_NOTEBOOK

        if content:
            validation_error: dict = {}
            with self.filesystem.open_input_file(fi.path) as fp:
                nb = nbformat.read(
                    fp,
                    as_version=4,
                    capture_validation_error={},
                )
            self.mark_trusted_cells(nb, path)
            model["content"] = nb
            model["format"] = "json"
            self.validate_notebook_model(model, validation_error)

        return model

    def get(
        self,
        path: str,
        content: bool = True,
        type: str | None = None,
        format: str | None = None,
        fi: fs.FileInfo | None = None,
    ) -> dict[str, Any]:
        path = path.strip('/')
        self.log.debug("get path=%s content=%s type=%s format=%s", path, content, type, format)

        four_o_four = f"file or directory does not exist: {path}"

        if (fi is None and not self.exists(path)) or (fi is not None and fi.type is fs.FileType.NotFound):
            raise web.HTTPError(404, four_o_four)

        if not self.allow_hidden and self.is_hidden(path):
            self.log.info("Refusing to serve hidden file or directory %s, via 404 Error", path)
            raise web.HTTPError(404, four_o_four)

        if fi is None:
            fi = self._get_file_info(path)

        if fi.type is fs.FileType.Directory and type in (None, MODEL_TYPE_DIRECTORY):
            model = self._dir_model(fi, path, content=content)
        elif (
            fi.type is fs.FileType.File
            and type == MODEL_TYPE_NOTEBOOK
            or (type is None and path.endswith(NOTEBOOK_EXTENSION))
        ):
            model = self._notebook_model(fi, path, content=content)
        else:
            model = self._file_model(fi, path, content=content, format=format)

        self.emit(data={"action": "get", "path": path})
        return model

    def save(self, model: dict[str, Any], path: str) -> dict[str, Any]:
        path = path.strip("/")
        self.log.debug("save %s at %s", model['type'], path)
        self.run_pre_save_hook(model=model, path=path)

        if "type" not in model:
            raise web.HTTPError(400, "No file type provided")
        if "content" not in model and model["type"] != MODEL_TYPE_DIRECTORY:
            raise web.HTTPError(400, "No file content provided")

        absolute_path = self._abs_path(path)

        if not self.allow_hidden and self.is_hidden(path):
            raise web.HTTPError(400, f"Cannot create file or directory {path!r}")

        validation_error: dict = {}
        try:
            if model["type"] == MODEL_TYPE_NOTEBOOK:
                nb = nbformat.from_dict(model["content"])
                self.check_and_sign(nb, path)
                with self.filesystem.open_output_stream(absolute_path) as stream:
                    s = nbformat.writes(nb, version=nbformat.NO_CONVERT, capture_validation_error=validation_error)
                    if not isinstance(s, bytes):
                        s = s.encode("utf8")

                    stream.write(s)

                # One checkpoint should always exist for notebooks.
                if not self.checkpoints.list_checkpoints(path):
                    self.create_checkpoint(path)
            elif model["type"] == MODEL_TYPE_FILE:
                format = model.get("format")
                if format not in {"text", "base64"}:
                    raise HTTPError(
                        400,
                        "Must specify format of file contents as 'text' or 'base64'",
                    )
                try:
                    if format == "text":
                        bcontent = model["content"].encode("utf8")
                    else:
                        b64_bytes = model["content"].encode("ascii")
                        bcontent = decodebytes(b64_bytes)

                    with self.filesystem.open_output_stream(absolute_path) as stream:
                        stream.write(bcontent)

                except Exception as e:
                    raise HTTPError(400, f"Encoding error saving {path}: {e}") from e
            elif model["type"] == MODEL_TYPE_DIRECTORY:
                self.filesystem.create_dir(absolute_path)
            else:
                raise web.HTTPError(400, "Unhandled contents type: %s" % model["type"])
        except web.HTTPError:
            raise
        except Exception as e:
            self.log.error("Error while saving file: %s %s", path, e, exc_info=True)
            raise web.HTTPError(500, f"Unexpected error while saving file: {path} {e}") from e

        validation_message = None
        if model["type"] == MODEL_TYPE_NOTEBOOK:
            self.validate_notebook_model(model, validation_error=validation_error)
            validation_message = model.get("message", None)

        model = self.get(path, content=False)
        if validation_message:
            model["message"] = validation_message

        self.run_post_save_hooks(model=model, os_path=absolute_path)
        self.emit(data={"action": "save", "path": path})
        return model

    def rename_file(self, old_path: str, new_path: str) -> dict[str, Any]:
        self.log.debug(f"rename {old_path} to {new_path}")

        if new_path == old_path:
            return

        if not self.allow_hidden and (self.is_hidden(old_path) or self.is_hidden(new_path)):
            raise web.HTTPError(400, f"Cannot rename file or directory {old_path!r}")

        abs_old_path = self._abs_path(old_path)
        abs_new_path = self._abs_path(new_path)
        fi = self.filesystem.get_file_info(abs_old_path)
        fi_new = self.filesystem.get_file_info(abs_new_path)

        # Should we proceed with the move?
        if fi_new.type is not fs.FileType.NotFound:
            raise web.HTTPError(409, "File already exists: %s" % new_path)

        if fi.type is fs.FileType.File:
            self.filesystem.move(abs_old_path, abs_new_path)
        elif fi.type is fs.FileType.Directory:
            # pyarrow s3 does not implement moving directories
            self.filesystem.create_dir(abs_new_path)
            file_infos = self.filesystem.get_file_info(fs.FileSelector(abs_old_path, recursive=True))
            directories = [fi for fi in file_infos if fi.type is fs.FileType.Directory]
            for directory in directories:
                self.filesystem.create_dir(directory.path.replace(abs_old_path, abs_new_path, 1))
            files = [fi for fi in file_infos if fi.type is fs.FileType.File]
            for file_ in files:
                dst = fi.path.replace(abs_old_path, abs_new_path, 1)
                self.filesystem.move(file_.path, dst)  # FIXME: add check
            self.filesystem.delete_dir(fi.path)
        else:
            raise NotImplementedError

    def delete_file(self, path: str) -> None:
        absolute_path = self._abs_path(path)
        fi = self.filesystem.get_file_info(absolute_path)
        if fi.type is fs.FileType.File:
            self.filesystem.delete_file(fi.path)
        elif fi.type is fs.FileType.Directory:
            self.filesystem.delete_dir(fi.path)
        else:
            raise NotImplementedError

    def is_hidden(self, path: str) -> bool:
        return os.path.basename(path).startswith(".")

    def _abs_path(self, path: str) -> str:
        absolute_path = os.path.join(self.root_dir, path.strip('/'))
        return self.filesystem.normalize_path(absolute_path)

    def _get_file_info(self, path: str) -> fs.FileInfo:
        absolute_path = self._abs_path(path)
        return self.filesystem.get_file_info(absolute_path)

    def file_exists(self, path: str = "") -> bool:
        self.log.debug(f"file_exists at {path}")
        absolute_path = self._abs_path(path)
        fi = self.filesystem.get_file_info(absolute_path)
        return fi.type is fs.FileType.File

    def dir_exists(self, path: str) -> bool:
        self.log.debug(f"dir_exists at {path}")
        absolute_path = self._abs_path(path)
        fi = self.filesystem.get_file_info(absolute_path)
        return fi.type is fs.FileType.Directory

    def _checkpoints_class_default(self) -> Type[Checkpoints]:
        return GenericFileCheckpoints
