import os
from typing import Any, Optional, Dict, Type
import aiofiles
from starlette.datastructures import UploadFile
from contracts.filesystem import Cloud


class PathPreFixer(object):
    def __init__(self, prefix: str, separator: str = '/'):
        self.prefix = prefix.rstrip('\\/')
        if self.prefix != '' or self.prefix == separator:
            self.prefix = self.prefix + separator
        self.separator = separator

    def prefix_path(self, path: str):
        return self.prefix + path.rstrip('/')


class FilesystemAdapter(Cloud):
    def __init__(self, driver: Any, adapter, config):
        self.driver = driver
        self.adapter = adapter
        self.config = config
        self.prefixer = PathPreFixer(config.get('root') or '', config.get('directory_separator') or '/')

    def url(self, path):
        adapter = self.adapter
        if hasattr(adapter, 'get_url'):
            return adapter.get_url(path=path)
        return self.get_local_url(path)

    def get_local_url(self, path):
        url = self.config.get('url')
        if url:
            return self.concat_path_to_url(url=url, path=path)
        path = f'/storage/{path}'
        if path.__contains__('/storage/public/'):
            return path.replace('/public/', '/')
        return path

    @staticmethod
    def concat_path_to_url(url, path):
        return url.rstrip('/') + '/' + path.lstrip('/')

    def exists(self, path: str):
        return os.path.exists(self.prefixer.prefix_path(path))

    def path(self, path: str):
        return self.prefixer.prefix_path(path)

    def get(self, path: str):
        pass

    def read_stream(self, path: str):
        pass

    async def put(self, path: str, content: Any, options: Optional[Dict] = None):
        options = {'visibility': options} if options is str else options
        await self.ensure_directory_exists(path)
        if isinstance(content, UploadFile):
            return await self.put_file(path, content)
        try:
            if isinstance(content, bytes):
                await self.write_stream(path, content)
            else:
                await self.write(path, content)
        except Exception as e:
            raise e
        return True

    async def put_file(self, path, file, options: Optional[Dict] = None):
        return await self.put_file_as(path, file, file.filename, options)

    async def put_file_as(self, path: str, file: Any, name: str, options: Optional[Dict] = None):
        stream = await file.read()
        await self.put(f'{path}'.rstrip('/'), stream, options)

    async def write(self, path: str, content: str):
        location = self.prefixer.prefix_path(path)
        async with aiofiles.open(location, mode='w') as f:
            await f.write(content)

    async def write_stream(self, path, resource: bytes, options: Optional[Dict] = None):
        location = self.prefixer.prefix_path(path)
        async with aiofiles.open(location, mode='wb') as f:
            await f.write(resource)

    def prepend(self, data: str):
        pass

    def append(self, data: str):
        pass

    def delete(self, paths: list[str]):
        pass

    def copy(self, src: str, to: str):
        pass

    def move(self, src: str, to: str):
        pass

    def size(self, path: str):
        pass

    def all_files(self, directory: str):
        pass

    def directories(self, directory: str = None, recursive: bool = False):
        pass

    def all_directories(self, directory: str = None):
        pass

    async def make_directory(self, path: str, mode=0o755, recursive=False, force=False):
        if force:
            os.makedirs(path)
            return True
        os.makedirs(path)
        return True

    async def ensure_directory_exists(self, path, mode: int = 0o755, recursive=True):
        directory = self.prefixer.prefix_path(os.path.dirname(path))
        if not os.path.exists(directory):
            await self.make_directory(directory, mode, recursive)

    def delete_directory(self, directory: str):
        pass

    def is_directory(self, directory: str):
        return os.path.isdir(directory)
