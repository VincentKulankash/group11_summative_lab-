"""JSON persistence layer. Owner: Vincent Kulankash."""
import json
import os

#json for reading/writing JSON
#os for path joining and filename existence checks
class Storage:
    """Read/write lists of objects as JSON files."""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)

    #This checks if we have the folder data where we will use it to save our filename and json objects

    def _path(self, filename: str) -> str:
        """Full path to a file inside the data folder"""
        return os.path.join(self.data_dir, filename)

    def save(self, filename: str, items: list) -> None:
        """Save a list of model objects to a json file"""

        with open(self._path(filename), "w") as f:
            json.dump([item.to_dict() for item in items], f, indent=2)
    #with open(self._path(filename)) opens the full filepath data/users.json and then 
    #no return this is used only to write 

    def load(self, filename: str, model_cls) -> list:
        """Load a json file and reconstruct objects via model_cls.from_dict()"""
        
        path = self._path(filename)
        if not os.path.exists(path):
            return []
        try:
            with open(path) as f:
                return [model_cls.from_dict(d) for d in json.load(f)]
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            print (f"Could not load {filename}: {e}")
            return []

#this file is polymorphic it accepts any list of obkects and calls .to_dict() on each