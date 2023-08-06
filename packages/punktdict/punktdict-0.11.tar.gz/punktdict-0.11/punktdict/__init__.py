import sys

dictconfig = sys.modules[__name__]
# Create a reference to the current module's `sys.modules` dictionary,
# which allows accessing and modifying the configuration options.

dictconfig.allow_nested_attribute_creation = True
# Set the configuration option `allow_nested_attribute_creation` to True,
# allowing the creation of nested attributes in PunktDict objects.

dictconfig.allow_nested_key_creation = True
# Set the configuration option `allow_nested_key_creation` to True,
# allowing the creation of nested keys in PunktDict objects.

dictconfig.convert_all_dicts_recursively = True
# Set the configuration option `convert_all_dicts_recursively` to True,
# enabling recursive conversion of all nested dictionaries in PunktDict objects.


def check_if_compatible_dict(di, class_):
    """
    Check if the provided object is a compatible dictionary based on its type and attributes.

    Args:
    - di: The object to check for compatibility.
    - class_: The class representing the compatible dictionary type.

    Returns:
    - True if the object is a compatible dictionary, False otherwise.


    """
    return (isinstance(di, dict) and not isinstance(di, class_)) or (
        (hasattr(di, "items") and hasattr(di, "keys") and hasattr(di, "values"))
    )


def convert_to_dict(di):
    """
    Recursively converts a PunktDict object or a compatible dictionary to a regular dictionary.

    Args:
    - di: The PunktDict object or compatible dictionary to convert.

    Returns:
    - The converted regular dictionary.
    """
    if isinstance(di, dict) or (
        hasattr(di, "items") and hasattr(di, "keys") and hasattr(di, "values")
    ):
        di = {k: convert_to_dict(v) for k, v in di.items()}
    return di


class PunktDict(dict):
    """
    A subclass of dict with additional functionality for handling nested dictionaries.

    Overrides some methods and provides additional methods to handle nested dictionaries.

    Attributes:
    - allow_nested_attribute_creation: A boolean flag indicating whether PunktDict allows creation of nested attributes.
    - allow_nested_key_creation: A boolean flag indicating whether PunktDict allows creation of nested keys.
    - convert_all_dicts_recursively: A boolean flag indicating whether PunktDict recursively converts all nested dictionaries to PunktDict objects.

    Methods:
    - __init__(self, *args, **kwargs): Initializes a new PunktDict object.
    - __setitem__(self, key, value): Sets an item in the PunktDict.
    - __missing__(self, key): Handles missing key access in the PunktDict.
    - update(self, *args, **kwargs): Updates the PunktDict with new data.
    - _check_forbidden_key(self, *args, **kwargs): Checks if a key is forbidden.
    - __getattr__(self, item): Handles attribute access in the PunktDict.


    """

    def __init__(self, *args, **kwargs):
        """
        Initializes a new PunktDict object.

        Args:
        - *args: Variable length argument list.
        - **kwargs: Arbitrary keyword arguments.

        Notes:
        - Converts all nested dictionaries in the PunktDict object to PunktDict objects
          if the `convert_all_dicts_recursively` option is enabled.
        - Maps the PunktDict object itself to its `__dict__` attribute.
        """

        def convert_dict(di):
            """
            Recursively converts a compatible dictionary to a PunktDict object.

            Args:
            - di: The compatible dictionary to convert.

            Returns:
            - The converted PunktDict object.
            """
            if check_if_compatible_dict(di, self.__class__):
                ndi = self.__class__({})
                for k, v in di.items():
                    ndi[k] = convert_dict(v)
                return ndi
            return di

        super().__init__(*args, **kwargs)
        if dictconfig.convert_all_dicts_recursively:
            for key in self:
                if key not in dir(dict):
                    self[key] = convert_dict(self[key])
        self.__dict__ = self

    def __setitem__(self, key, value):
        """
        Sets an item in the PunktDict.

        Args:
        - key: The key to set.
        - value: The value to assign to the key.

        Notes:
        - Converts the value to a PunktDict object if it is a compatible dictionary
          and the `convert_all_dicts_recursively` option is enabled.
        - Raises a ValueError if the key is not allowed.
        """
        if dictconfig.convert_all_dicts_recursively:
            if check_if_compatible_dict(value, self.__class__):
                value = self.__class__(value)
        if key not in dir(dict):
            super().__setitem__(key, value)
        else:
            raise ValueError(f'Key "{key}" not allowed!')

    def __missing__(self, key):
        """
        Handles missing key access in the PunktDict.

        Args:
        - key: The missing key.

        Returns:
        - The created nested PunktDict if `allow_nested_key_creation` is enabled.

        Raises:
        - KeyError: If `allow_nested_key_creation` is disabled and the key is not found.
        """
        if dictconfig.allow_nested_key_creation:
            self[key] = self.__class__({})
            return self[key]
        raise KeyError(f'"{key}" not found')

    def update(self, *args, **kwargs) -> None:
        """
        Updates the PunktDict with new data.

        Args:
        - *args: Variable length argument list.
        - **kwargs: Arbitrary keyword arguments.

        Notes:
        - Converts all nested dictionaries in the new data to PunktDict objects
          if the `convert_all_dicts_recursively` option is enabled.
        """
        if dictconfig.convert_all_dicts_recursively:
            args = [self.__class__(x) for x in args]
        super().update(*args, **kwargs)

    def _check_forbidden_key(self, *args, **kwargs):
        """
        Checks if a key is forbidden.
        Method can be overwritten

        Args:
        - *args: Variable length argument list.
        - **kwargs: Arbitrary keyword arguments.

        Returns:
        - False always.
        """
        return False

    def __getattr__(self, item):
        """
        Handles attribute access in the PunktDict.

        Args:
        - item: The attribute name.

        Returns:
        - The created nested PunktDict if `allow_nested_attribute_creation` is enabled.

        Raises:
        - AttributeError: If `allow_nested_attribute_creation` is disabled or the attribute is forbidden.
        """
        if not self._check_forbidden_key(item):
            if dictconfig.allow_nested_attribute_creation:
                self[item] = self.__class__({})
                return self[item]
        raise AttributeError
