#!/usr/bin/python3

"""
This file defines the storage system for
the project.
It will use JSON format to either serialize and deserialize objects
"""

import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review



class FileStorage:
    """
        This is  will serve as an Object relation mappingto interface or database
    """
    __file_path = r"C:\Users\Dedo-PC\Desktop\AirBnB_clone\models\engine\file_storage.py"
    __objects = {}

    def all(self):
        """Returns the dictionary __objects"""
        return self.__objects

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id"""
        key = obj.__class__.__name__ + '.' + obj.id
        self.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file (path: __file_path)"""
        serialized_objects = {}
        for key, obj in self.__objects.items():
            serialized_objects[key] = obj.to_dict()
        with open(self.__file_path, 'w') as file:
            json.dump(serialized_objects, file)

    def reload(self):
        """Deserializes the JSON file to __objects"""
        try:
            with open(self.__file_path, 'r') as file:
                serialized_objects = json.load(file)
                for key, obj_dict in serialized_objects.items():
                    class_name, obj_id = key.split('.')
                    obj = globals()[class_name](**obj_dict)
                    self.__objects[key] = obj
        except FileNotFoundError:
            pass

def _deserialize(self, obj):
        """Deserialize JSON string to object"""
        if '__class__' in obj:
            class_name = obj['__class__']
            del obj['__class__']
            if class_name == 'User':
                return User(**obj)
            elif class_name == 'BaseModel':
                return BaseModel(**obj)
            elif class_name == 'State':
                return State(**obj)
            elif class_name == 'City':
                return City(**obj)
            elif class_name == 'Amenity':
                return Amenity(**obj)
            elif class_name == 'Place':
                return Place(**obj)
            elif class_name == 'Review':
                return Review(**obj)

        return obj