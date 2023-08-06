from typing import Any, Optional, Dict, Type
from starlette.datastructures import UploadFile
from filesystem.filesystem_adapter import FilesystemAdapter
from obs import ObsClient


class ObsAdapter(FilesystemAdapter):
    def __init__(self, adapter, config, client: ObsClient, driver='obs'):
        super().__init__(driver, adapter, config)
        self.client = client

    def get_url(self, path):
        ret = self.client.getObject(bucketName='xjguoyu', objectKey=path)
        print(ret)
        return ''

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
