#!/usr/bin/env python3
"""
FileStorage class for storing models in a file-based system.
"""
import json
from models.base import Base

class FileStorage:
    """Class to simulate storage of objects in a file."""
    
    __file_path = "db.json"
    __objects = {}

    def all(self):
        """Returns the dictionary of all objects."""
        return FileStorage.__objects

    def new(self, obj):
        """Adds a new object to the storage."""
        if obj:
            key = f"{obj.__class__.__name__}.{obj.id}"
            FileStorage.__objects[key] = obj

    def save(self):
        """Saves all objects to a file."""
        with open(FileStorage.__file_path, "w") as f:
            json.dump(FileStorage.__objects, f)

    def reload(self):
        """Reloads all objects from a file."""
        try:
            with open(FileStorage.__file_path, "r") as f:
                FileStorage.__objects = json.load(f)
        except FileNotFoundError:
            FileStorage.__objects = {}

    def get(self, cls, id):
        """Gets an object by class and id."""
        key = f"{cls.__name__}.{id}"
        return FileStorage.__objects.get(key)

    def delete(self, obj):
        """Deletes an object from storage."""
        key = f"{obj.__class__.__name__}.{obj.id}"
        if key in FileStorage.__objects:
            del FileStorage.__objects[key]
