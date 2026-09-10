"""JSON persistence layer. Owner: YOU."""
import json
import os


class Storage:
    """Read/write lists of objects as JSON files."""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)

    def _path(self, filename: str) -> str:
        return os.path.join(self.data_dir, filename)

    def save(self, filename: str, items: list) -> None:
        """Persist list of objects (each with .to_dict()) to JSON."""
        # TODO (YOU)
        with open(self._path(filename), "w") as f:
            json.dump([i.to_dict() for i in items], f, indent=2)

    def load(self, filename: str, model_cls) -> list:
        """Load list of objects using model_cls.from_dict()."""
        # TODO (YOU): handle missing file + corrupt JSON
        path = self._path(filename)
        if not os.path.exists(path):
            return []
        try:
            with open(path) as f:
                return [model_cls.from_dict(d) for d in json.load(f)]
        except (json.JSONDecodeError, KeyError, TypeError):
            return []