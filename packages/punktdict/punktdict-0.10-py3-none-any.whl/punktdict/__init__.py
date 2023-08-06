def convert_back(di):
    if isinstance(di, dict) or (
        hasattr(di, "items") and hasattr(di, "keys") and hasattr(di, "keys")
    ):
        di = {k: convert_back(v) for k, v in di.items()}
    return di


_extra_methods_and_attributes = (
    "_check_forbidden_key",
    "convert_to_regular_dict",
    "_allow_nested_creation",
)


class PunktDict(dict):
    """
    A dictionary-like object with extended functionality.

    This class is a subclass of the built-in `dict` class. It adds several features and overrides
    certain methods to provide additional behavior.

    Attributes:
        _allow_nested_creation: whether to allow nested key creation:
            if True, this will work:
            dd["school"]["room2"]["student1"] = "Bruno"
            dd.school.room3.student1 = "Bruno"

    Methods:
        __new__(cls, o=None, *args, **kwargs): Overrides the creation of a new instance of `PunktDict`.
        __init__(self, seq=None, **kwargs): Initializes a `PunktDict` instance.
        _check_forbidden_key(self, *args, **kwargs): Checks if a key is forbidden.
        __setattr__(self, key, value): Overrides the setting of an attribute.
        __delitem__(self, key): Overrides the deletion of an item.
        __getitem__(self, item): Overrides the retrieval of an item.
        __setitem__(self, key, value): Overrides the assignment of an item.
        __delattr__(self, item): Overrides the deletion of an attribute.
        __missing__(self, key): Overrides the handling of missing keys.
        __getattribute__(self, name): Overrides the retrieval of an attribute.
        __getattr__(self, item): Overrides the retrieval of a missing attribute.
        convert_to_regular_dict: Converts the PunktDict to a regular dict

    Usage:
        # Create a new instance of PunktDict
        dd = PunktDict({'school': {'room1': {'student1': 'Mario', 'student2': 'Mario'}}})

        # Access and modify values using dictionary-like syntax
        dd['school']['room1']['student6'] = 'Antonio'
        dd['school']['room2']['student1'] = 'Bruno'
        dd.school.room3.student1 = 'Bruno'

        # Delete an item
        del dd['school']['room2']['student1']

        # Access and modify attributes using dot notation
        dd.university.all_rooms = []
        dd.university.all_rooms.append(1)
        dd['university']['all_rooms'].append(2)
        dd.university['all_rooms'].append(3)

        # Print the PunktDict object
        print(dd)
    """

    def __new__(cls, seq=None, allow_nested_creation=True, *args, **kwargs):
        # Create a new instance of the class
        new_dict = super().__new__(cls, seq)
        new_dict._allow_nested_creation = allow_nested_creation
        if seq:
            # Check if the keys are strings and set them as attributes of the object
            for key, item in new_dict.items():
                if isinstance(key, str):
                    if not hasattr(new_dict, key):
                        try:
                            new_dict.__setattr__(key, item)
                        except (TypeError, ValueError):
                            continue

        return new_dict

    def __init__(self, seq=None, allow_nested_creation=True, **kwargs):
        if seq:
            # Initialize the dictionary with the given sequence
            super().__init__(seq, **kwargs)

        def convert_dict(di):
            if (isinstance(di, dict) and not isinstance(di, self.__class__)) or (
                (hasattr(di, "items") and hasattr(di, "keys") and hasattr(di, "keys"))
            ):
                # Convert nested dictionaries to PunktDict instances recursively
                ndi = self.__class__({}, allow_nested_creation=allow_nested_creation)
                for k, v in di.items():
                    ndi[k] = convert_dict(v)
                return ndi
            return di

        for key in self:
            if key not in dir(dict) and key not in _extra_methods_and_attributes:
                # Convert non-dictionary values to PunktDict instances
                self[key] = convert_dict(self[key])

    def _check_forbidden_key(self, *args, **kwargs):
        # can be overwritten like:
        # PunktDict._check_forbidden_key = lambda self, x: x.startswith('_ipytho') or x == '_repr_mimebundle_'
        # to prevent accidental dict creation when _allow_nested_creation is True, if the function returns True, the key will not be created
        return False

    def __setattr__(self, key, value):
        if key in dir(dict):
            raise KeyError
        # Set an attribute and an item with the same key
        if key not in dir(dict):
            super().__setattr__(key, value)

        if key not in _extra_methods_and_attributes:
            super().__setitem__(key, value)

    def update(self, *args, **kwargs) -> None:
        allargs = [self.__class__(x) for x in args]
        super().update(*allargs, **kwargs)

    def __delitem__(self, key):
        # Delete an item and its corresponding attribute (if it exists)
        super().__delitem__(key)
        if isinstance(key, str):
            if hasattr(self, key):
                if key not in dir(dict) and key not in _extra_methods_and_attributes:
                    super().__delattr__(key)

    def __getitem__(self, item):
        try:
            # Get an item using dictionary-like syntax
            return super().__getitem__(item)
        except KeyError:
            if item not in dir(dict) and item not in _extra_methods_and_attributes:
                # If the key doesn't exist, create an empty PunktDict instance for that key
                self.__setitem__(item, self.__class__())
                return self.__getitem__(item)

    def __setitem__(self, key, value):
        # Set an item using dictionary-like syntax
        if isinstance(value, dict) and not isinstance(value, self.__class__):
            print(value)
            value = self.__class__(value)
        super().__setitem__(key, value)
        if isinstance(key, str):
            if key not in dir(dict) and key not in _extra_methods_and_attributes:
                try:
                    # Set an attribute with the same key
                    self.__setattr__(key, self[key])
                except (TypeError, ValueError):
                    pass

    def __delattr__(self, item):
        # Delete an attribute and its corresponding item (if it exists)
        if item not in dir(dict) and item not in _extra_methods_and_attributes:
            super().__delattr__(item)
        if item in self:
            del self[item]

    def __missing__(self, key):
        # Handle missing keys by creating an empty PunktDict instance for that key
        if not self._allow_nested_creation:
            raise KeyError
        if key not in dir(dict) and key not in _extra_methods_and_attributes:
            self[key] = self.__class__({})
            return self[key]

    def __getattribute__(self, name):
        if name in dir(dict) or name in _extra_methods_and_attributes:
            return super().__getattribute__(name)
        if name in self:
            # Get an attribute using dot notation
            return self[name]
        return super().__getattribute__(name)

    def __getattr__(self, item):
        if not self._allow_nested_creation:
            raise KeyError
        if not self._check_forbidden_key(item):
            # If the attribute doesn't exist, create an empty PunktDict instance for that attribute
            self.__setitem__(item, self.__class__())
        return self.__getattribute__(item)

    def convert_to_regular_dict(self):
        return convert_back(self)


