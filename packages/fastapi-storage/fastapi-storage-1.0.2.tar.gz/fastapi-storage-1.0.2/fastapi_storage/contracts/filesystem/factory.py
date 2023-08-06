from abc import abstractmethod


class Factory:
    @abstractmethod
    def disk(self, name=None):
        pass
