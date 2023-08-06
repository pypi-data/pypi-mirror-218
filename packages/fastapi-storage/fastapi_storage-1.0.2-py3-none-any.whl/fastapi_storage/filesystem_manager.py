from typing import Any

import oss2
from obs import ObsClient
from operator import methodcaller
from config.filesystems import filesystems
from contracts.filesystem.factory import Factory
from filesystem.filesystem_adapter import FilesystemAdapter
from filesystem.obs_adapter import ObsAdapter
from filesystem.oss_adapter import OssAdapter


class FilesystemManager(Factory):
    disks: dict = {}

    def __new__(cls, *args, **kwargs) -> Any:
        return cls.disk()

    @classmethod
    def drive(cls, name=None):
        return cls.disk(name=name)

    @classmethod
    def disk(cls, name=None):
        name = name or cls.get_default_drive()
        cls.disks[name] = cls.get(name)
        return cls.disks[name]

    @classmethod
    def get(cls, name):
        return cls.disks.get(name) or cls.resolve(name)

    @classmethod
    def resolve(cls, name, config=None):
        config = config or cls.get_config(name)
        name = config.get('driver')
        driver_method = f'create_{name}_driver'
        if hasattr(cls, driver_method):
            return methodcaller(driver_method, config)(cls)
        return

    @classmethod
    def cloud(cls):
        name = cls.get_default_cloud_driver()
        return cls.disks[name]

    @staticmethod
    def get_default_drive():
        return filesystems.default

    @staticmethod
    def get_default_cloud_driver():
        return filesystems.disks.cloud

    @staticmethod
    def get_config(name=None):
        return filesystems.disks.dict().get(name) or {}

    @classmethod
    def create_local_driver(cls, config):
        return FilesystemAdapter(driver={}, adapter={}, config=config)

    @classmethod
    def create_obs_driver(cls, config):
        client = ObsClient(
            access_key_id=config['access_key_id'],
            secret_access_key=config['secret_access_key'],
            server=config['server']
        )
        adapter = ObsAdapter(config=config, adapter={}, client=client)
        return FilesystemAdapter(driver={}, adapter=adapter, config=config)

    @classmethod
    def create_oss_driver(cls, config):
        auth = oss2.Auth(config['access_key'], config['secret_key'])
        bucket = oss2.Bucket(auth, config['endpoint'], config['bucket'], is_cname=config['is_cname'])
        return OssAdapter(config=config, adapter={}, client=bucket)
