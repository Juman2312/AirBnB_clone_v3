#!/usr/bin/python3

"""
This file defines  the BaseModel class which will
serve as the base of ou model.
"""
import uuid
from datetime import datetime
from models import storage

class BaseModel:
    """Base class for all our classes"""

    def __init__(self, *args, **kwargs):
        """Add a call to the method new(self) on storage"""
        if kwargs:
            self.__set_attributes(kwargs)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)

    def __set_attributes(self, attributes):
        """Set the attributes"""
        for key, value in attributes.items():
            if key != "__class__":
                if key == "created_at" or key == "updated_at":
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                setattr(self, key, value)


    def save(self):
        """Call save() method of storage"""
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        attributes = self.__dict__.copy()
        attributes["__class__"] = self.__class__.__name__
        attributes["created_at"] = attributes["created_at"].isoformat()
        attributes["updated_at"] = attributes["updated_at"].isoformat()
        return attributes
