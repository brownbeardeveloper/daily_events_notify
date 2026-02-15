from pathlib import Path
import json

from .schemas import BaseEvents


class JsonFileManager:
    def __init__(self, file_path: Path):
        self._file_path: Path = file_path
        self._data: list[BaseEvents] = self._load_json()

    def _load_json(self) -> list[BaseEvents]:
        if not self._file_path.exists():
            raise FileNotFoundError("File not found")
        
        with open(self._file_path, "r") as f:
            return [BaseEvents(**item) for item in json.load(f)]

    def _save_json(self) -> None:
        if self._data is None:
            raise ValueError("Data cannot be None")
        
        with open(self._file_path, "w") as f:
            json.dump([item.model_dump(mode="json") for item in self._data], f)

    def _next_id(self) -> int:
        if not self._data:
            return 0
        return max(item.id for item in self._data) + 1

    def _find_index(self, key: int) -> int:
        for i, item in enumerate(self._data):
            if item.id == key:
                return i
        raise KeyError("Key not found")
    
    def get_data_by_id(self, key: int) -> BaseEvents:
        idx = self._find_index(key)
        return self._data[idx].model_copy()

    def get_all_data(self) -> list[BaseEvents]:
        return self._data.copy()

    def add_new_data(self, value: BaseEvents) -> None:
        if not isinstance(value, BaseEvents):
            raise ValueError("Value must be of type BaseEvents")
        if value.id is not None and any(item.id == value.id for item in self._data):
            raise ValueError("Key already exists")
        value.id = self._next_id()
        self._data.append(value)
        self._save_json()
    
    def update_data(self, key: int, value: BaseEvents) -> None:
        if not isinstance(value, BaseEvents):
            raise ValueError("Value must be of type BaseEvents")
        idx = self._find_index(key)
        value.id = key
        self._data[idx] = value
        self._save_json()

    def delete_data(self, key: int) -> None:
        idx = self._find_index(key)
        del self._data[idx]
        self._save_json()