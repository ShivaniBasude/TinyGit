from tinygit import objects

class Blob:
    def __init__(self, data: bytes):
        self.data = data
        
    @classmethod
    def from_file(cls, path: str) -> 'Blob':
        with open(path, "rb") as f:
            return cls(f.read())
            
    def save(self) -> str:
        """Saves the blob to the object store and returns its SHA-1."""
        return objects.write_object(self.data, "blob")
