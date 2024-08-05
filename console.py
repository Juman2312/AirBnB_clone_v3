#!/usr/bin/python3
""" Defines the console class
which is the entry point of the Airbnb Project
"""


import cmd
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review



class HBNBCommand(cmd.Cmd):
    """Defines the HolbertonBnB command interpreter.
    Attributes:
        prompt (str): The command prompt.
    """

    prompt = "(hbnb) "
    valid_classes = ['BaseModel', 'User', 'State', 'City', 'Amenity', 'Place', 'Review']

    def do_create(self, arg):
        """Create a new instance of a class"""
        if not arg:
            print("** class name missing **")
            return
        arg = arg.split()
        class_name = arg[0]
        if class_name not in self.valid_classes:
            print("** class doesn't exist **")
            return
        new_obj = eval(class_name)()
        new_obj.save()
        print(new_obj.id)

    def do_show(self, arg):
        """Show an instance based on the class name and id"""
        if not arg:
            print("** class name missing **")
            return
        arg = arg.split()
        class_name = arg[0]
        if class_name not in self.valid_classes:
            print("** class doesn't exist **")
            return
        if len(arg) < 2:
            print("** instance id missing **")
            return
        obj_id = arg[1]
        key = class_name + "." + obj_id
        all_objs = storage.all()
        if key not in all_objs:
            print("** no instance found **")
            return
        print(all_objs[key])

    def do_destroy(self, arg):
        """Delete an instance based on the class name and id"""
        if not arg:
            print("** class name missing **")
            return
        arg = arg.split()
        class_name = arg[0]
        if class_name not in self.valid_classes:
            print("** class doesn't exist **")
            return
        if len(arg) < 2:
            print("** instance id missing **")
            return
        obj_id = arg[1]
        key = class_name + "." + obj_id
        all_objs = storage.all()
        if key not in all_objs:
            print("** no instance found **")
            return
        del all_objs[key]
        storage.save()

    def do_update(self, arg):
        """Update an instance based on the class name, id, attribute, and value"""
        if not arg:
            print("** class name missing **")
            return
        arg = arg.split()
        class_name = arg[0]
        if class_name not in self.valid_classes:
            print("** class doesn't exist **")
            return
        if len(arg) < 2:
            print("** instance id missing **")
            return
        obj_id = arg[1]
        key = class_name + "." + obj_id
        all_objs = storage.all()
        if key not in all_objs:
            print("** no instance found **")
            return
        if len(arg) < 3:
            print("** attribute name missing **")
            return
        if len(arg) < 4:
            print("** value missing **")
            return
        attribute = arg[2]
        value = arg[3]
        setattr(all_objs[key], attribute, value)
        all_objs[key].save()

    def do_all(self, arg):
        """Print all instances of a class or all classes"""
        arg = arg.split()
        if len(arg) == 0:
            all_objs = storage.all()
            print([str(obj) for obj in all_objs.values()])
        elif arg[0] in self.valid_classes:
            class_name = arg[0]
            all_objs = storage.all(class_name)
            print([str(obj) for obj in all_objs.values()])
        else:
            print("** class doesn't exist **")

    def do_quit(self, arg):
        """Quit the console"""
        return True

    def do_EOF(self, arg):
        """Quit the console using EOF (Ctrl+D)"""
        print()
        return True

    def emptyline(self):
        """Do nothing when an empty line is entered"""
        pass

if __name__ == '__main__':
    HBNBCommand().cmdloop()