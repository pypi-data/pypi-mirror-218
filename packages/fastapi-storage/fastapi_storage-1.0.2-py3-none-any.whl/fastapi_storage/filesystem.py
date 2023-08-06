import os


class Filesystem:
    @staticmethod
    def exists(path):
        return os.path.exists(path)
