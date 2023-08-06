# a dict with key attributes 

## pip install punktdict 

This module provides the `PunktDict` class, which is a subclass of dict with additional functionality for handling nested dictionaries. 
It also provides some configuration options through the `dictconfig` object.


```python
import sys
from punktdict import PunktDict, dictconfig, convert_to_dict

# Configure PunktDict behavior
dictconfig.allow_nested_attribute_creation = True
dictconfig.allow_nested_key_creation = True
dictconfig.convert_all_dicts_recursively = True
PunktDict._check_forbidden_key = (
    lambda self, x: (x.startswith("_ipython") or x == "_repr_mimebundle_")
)

# Create a PunktDict object
d = PunktDict({'popeye': {'mole': {'bole': 'dolle'}}})

# Access and modify nested dictionary values
d['hallo']['baba'] = 11
d.lll.ddd.xxx = 333

# Update PunktDict with new data
d.update({'rrrx': {'xxxxx': 'bbbb'}})
d.rrrx.xxxxxxx = []
d.rrrx.xxxxxxx.append(3)

# Access nested dictionary values using attribute syntax
d['gggg']['xxxxx']['tttt'] = 12
print(d.gggg.xxxxx.tttt)

# Convert PunktDict to a regular dictionary
di = convert_to_dict(d)
---------------

Attributes:
-----------
- allow_nested_attribute_creation: A boolean flag indicating whether PunktDict allows creation of nested attributes. Default is True.
- allow_nested_key_creation: A boolean flag indicating whether PunktDict allows creation of nested keys. Default is True.
- convert_all_dicts_recursively: A boolean flag indicating whether PunktDict recursively converts all nested dictionaries to PunktDict objects. Default is True.

Classes:
--------
- PunktDict: A subclass of dict with additional functionality for handling nested dictionaries.

Functions:
----------
- check_if_compatible_dict: Checks if an object is a compatible dictionary based on its type and attributes.
- convert_to_dict: Recursively converts a PunktDict object or a compatible dictionary to a regular dictionary.

Note:
-----
The `PunktDict` class overrides several methods and provides additional methods to handle nested dictionaries. The configuration options can be modified through the `dictconfig` object. The `convert_to_dict` function can be used to convert a PunktDict object or a compatible dictionary to a regular dictionary.

```