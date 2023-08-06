from pydantic import Field, BaseModel
from core.settings import Settings


class OSS(Settings):
    driver: str = 'oss'
    root: str = ''
    access_key: str = ''
    secret_key: str = ''
    endpoint: str = ''
    bucket: str = ''
    cdn_domain: str = ''
    ssl: bool = False
    debug: bool = False
    is_cname: bool = False

    class Config:
        env_prefix = 'oss_'


class OBS(Settings):
    driver: str = 'obs'
    access_key_id: str = ''
    secret_access_key: str = ''
    server: str = ''

    class Config:
        env_prefix = 'obs_'


class Local(BaseModel):
    driver: str = 'local'
    root: str = storage_path('app')


class Public(BaseModel):
    driver: str = 'local'
    root: str = storage_path('app/public')
    url: str = '/storage'
    visibility: str = 'public'


class Storage(BaseModel):
    driver: str = 'local'
    root: str = '/storage'
    url: str = '/storage'
    visibility: str = 'public'


class Disks(BaseModel):
    local: Local = Local()
    public: Public = Public()
    storage: Storage = Storage()
    oss: OSS = OSS()
    obs: OBS = OBS()


class Filesystems(Settings):
    default: str = Field('local', env='filesystem_disk')
    cloud: str = Field('local', env='filesystem_disk')
    disks: Disks = Disks()
    links: tuple = (public_path('storage'), storage_path('app/public'))


filesystems = Filesystems()
