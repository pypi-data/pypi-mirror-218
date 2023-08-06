from abc import abstractmethod, ABCMeta


class Filesystem(metaclass=ABCMeta):
    @abstractmethod
    def exists(self, path: str):
        pass

    @abstractmethod
    def get(self, path: str):
        pass

    @abstractmethod
    def read_stream(self, path: str):
        pass

    @abstractmethod
    def put(self, path: str, content: str, options):
        pass

    @abstractmethod
    def write_stream(self, path, resource: bytes, options):
        pass

    @abstractmethod
    def prepend(self, data: str):
        pass

    @abstractmethod
    def append(self, data: str):
        pass

    @abstractmethod
    def delete(self, paths: list[str]):
        pass

    @abstractmethod
    def copy(self, src: str, to: str):
        pass

    @abstractmethod
    def move(self, src: str, to: str):
        pass

    @abstractmethod
    def size(self, path: str):
        pass

    @abstractmethod
    def all_files(self, directory: str):
        pass

    @abstractmethod
    def directories(self, directory: str = None, recursive: bool = False):
        pass

    @abstractmethod
    def all_directories(self, directory: str = None):
        pass

    @abstractmethod
    def make_directory(self, path: str):
        pass

    @abstractmethod
    def delete_directory(self, directory: str):
        pass
