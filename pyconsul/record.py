
class PyconsulRecord:
    ' Encapsulates details about the key, path, value structure for Consul records '

    def __init__(self, key, path):
        self._key = key
        self._path = path

    @property
    def key(self):
        ' The base key '
        return self._key

    @property
    def path(self):
        ' The path for the file '
        return self._path

    @property
    def contents(self):
        ' Returns the contents of the file '
        return self._contents

    @contents.setter
    def contents(self, value):
        ' Sets the contents of the file. Done after construction to save memory '
        self._contents = value

    def __str__(self):
        return f"key={self._key}, path={self._path}, contents={self._contents}"
