from typing import Any, Optional, Dict, Type
from starlette.datastructures import UploadFile
from filesystem.filesystem_adapter import FilesystemAdapter
from oss2 import Bucket


class OssAdapter(FilesystemAdapter):
    def __init__(self, adapter, config, client: Bucket, driver='oss'):
        super().__init__(driver, adapter, config)
        self.client = client
        self.bucket = config['bucket']
        self.is_cname = config['is_cname']
        self.ssl = config['ssl']
        self.cdn_domain = config['cdn_domain']
        self.endpoint = config['endpoint']

    def get_bucket(self):
        return self.bucket

    def get_url(self, path):
        if not self.has(path):
            return 'not found'
        return ('https://' if self.ssl else "http://") + ((
                                                              self.endpoint if self.cdn_domain == '' else self.cdn_domain) if self.is_cname else self.bucket + '.' + self.endpoint) + '/' + path.lstrip(
            '/')

    async def put(self, path: str, content: Any, options: Optional[Dict] = None):
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

    async def write_stream(self, path, resource: bytes, options: Optional[Dict] = None):
        location = self.prefixer.prefix_path(path)
        self.client.put_object(path, resource)
        return path

    async def write(self, path: str, content: str):
        key = self.prefixer.prefix_path(path)
        self.client.put_object(key, content)
        return path

    def has(self, path: str):
        obj = self.prefixer.prefix_path(path)
        return self.client.object_exists(obj)
