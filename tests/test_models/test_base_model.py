#!/usr/bin/env python3
""" unittest for base model """


import unittest
from unittest.mock import patch
from io import StringIO
from datetime import datetime
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage


class TestFileStorage(unittest.TestCase):

    def setUp(self):
        # Create a temporary file path for testing
        self.file_path = "test_file.json"

    def tearDown(self):
        # Remove the temporary file after each test
        try:
            os.remove(self.file_path)
        except FileNotFoundError:
            pass

    def test_new_object_added_to_objects(self):
        storage = FileStorage()
        obj = BaseModel()
        storage.new(obj)
        objects = storage.all()
        self.assertIn(f"{obj.__class__.__name__}.{obj.id}", objects)

    def test_save_serializes_objects_to_file(self):
        storage = FileStorage()
        obj1 = BaseModel()
        obj2 = BaseModel()
        storage.new(obj1)
        storage.new(obj2)

        # Patch the `open` function to capture the file content
        with patch("builtins.open", create=True) as mock_open:
            storage.save()

            # Assert that the file was opened with the correct path
            mock_open.assert_called_once_with(storage._FileStorage__file_path, 'w')

            # Check if the serialized objects were written to the file
            file_content = mock_open.return_value.write.call_args[0][0]
            self.assertIn(obj1.id, file_content)
            self.assertIn(obj2.id, file_content)

    def test_reload_deserializes_objects_from_file(self):
        storage = FileStorage()
        obj = BaseModel()
        storage.new(obj)
        storage.save()

        # Patch the `open` function to return a file-like object with the serialized objects
        with patch("builtins.open", create=True) as mock_open:
            mock_open.return_value.__enter__.return_value.read.return_value = '{"BaseModel.' + obj.id + '": {"id": "' + obj.id + '", "created_at": "' + obj.created_at.isoformat() + '", "updated_at": "' + obj.updated_at.isoformat() + '"}}'

            storage.reload()

            # Check if the deserialized object is in the storage
            objects = storage.all()
            self.assertIn(f"{obj.__class__.__name__}.{obj.id}", objects)

    def test_save_and_reload_consistency(self):
        storage = FileStorage()
        obj = BaseModel()
        storage.new(obj)
        storage.save()
        storage.reload()
        objects_before = storage.all()

        # Modify the object after reloading
        obj.some_attribute = "some value"

        # Save and reload again
        storage.save()
        storage.reload()
        objects_after = storage.all()

        # Check if the modified object is still the same after reloading
        self.assertEqual(objects_before, objects_after)

if __name__ == "__main__":
    unittest.main()
