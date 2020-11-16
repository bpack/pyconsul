
class PyconsulRecord:

    def __init__(self, key, path):
        self._key = key
        self._path = path

    @property
    def key(self):
        return self._key

    @property
    def path(self):
        return self._path

    @property
    def contents(self):
        return self._contents

    @contents.setter
    def contents(self, value):
        self._contents = value

    def __str__(self):
        return f"key={self._key}, path={self._path}, contents={self._contents}"
