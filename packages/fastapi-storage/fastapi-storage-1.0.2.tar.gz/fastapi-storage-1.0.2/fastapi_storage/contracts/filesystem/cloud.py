from abc import abstractmethod
from contracts.filesystem.filesystem import Filesystem


class Cloud(Filesystem):
    @abstractmethod
    def url(self, path):
        pass
