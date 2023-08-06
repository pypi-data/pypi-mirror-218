# a dict with key attributes 

## pip install punktdict 

```python
# Example usage:
from punktdict import PunktDict
PunktDict._check_forbidden_key = (
    lambda self, x: x.startswith("_ipytho") or x == "_repr_mimebundle_"
)  # To avoid accidental creation of certain keys when allow_nested_creation is True

dd = PunktDict(
    {
        "school": {
            "room1": {
                "student1": "Mario",
                "student2": "Paulo",
                "student3": "Bernd",
                "student4": "Richard",
                "student5": "Mairo",
            }
        }
    },
    allow_nested_creation=True,
)
print(f"--------------------\n{dd}")
dd["school"]["room1"]["student6"] = "Antonio"
print(f"--------------------\n{dd}")
dd["school"]["room2"]["student1"] = "Bruno"
print(f"--------------------\n{dd}")
dd.school.room3.student1 = "Bruno"
print(f"--------------------\n{dd}")
del dd["school"]["room2"]["student1"]
print(f"--------------------\n{dd}")
dd.university.all_rooms = []
print(f"--------------------\n{dd}")
dd.university.all_rooms.append(1)
dd["university"]["all_rooms"].append(2)
dd.university["all_rooms"].append(3)
print(f"--------------------\n{dd}")
print(type(dd))
print(type(dd.convert_to_regular_dict()))

print(dd.random_new_key)  # creates a new key

try:
    print(dd._repr_mimebundle_)  # forbidden
except AttributeError as e:
    print(e)

try:
    dd.keys = 3333
except KeyError as e:
    print(e)

# {'school': {'room1': {'student1': 'Mario', 'student2': 'Paulo', 'student3': 'Bernd', 'student4': 'Richard', 'student5': 'Mairo'}}}
# --------------------
# {'school': {'room1': {'student1': 'Mario', 'student2': 'Paulo', 'student3': 'Bernd', 'student4': 'Richard', 'student5': 'Mairo', 'student6': 'Antonio'}}}
# --------------------
# {'school': {'room1': {'student1': 'Mario', 'student2': 'Paulo', 'student3': 'Bernd', 'student4': 'Richard', 'student5': 'Mairo', 'student6': 'Antonio'}, 'room2': {'student1': 'Bruno'}}}
# --------------------
# {'school': {'room1': {'student1': 'Mario', 'student2': 'Paulo', 'student3': 'Bernd', 'student4': 'Richard', 'student5': 'Mairo', 'student6': 'Antonio'}, 'room2': {'student1': 'Bruno'}, 'room3': {'student1': 'Bruno'}}}
# --------------------
# {'school': {'room1': {'student1': 'Mario', 'student2': 'Paulo', 'student3': 'Bernd', 'student4': 'Richard', 'student5': 'Mairo', 'student6': 'Antonio'}, 'room2': {}, 'room3': {'student1': 'Bruno'}}}
# --------------------
# {'school': {'room1': {'student1': 'Mario', 'student2': 'Paulo', 'student3': 'Bernd', 'student4': 'Richard', 'student5': 'Mairo', 'student6': 'Antonio'}, 'room2': {}, 'room3': {'student1': 'Bruno'}}, 'university': {'all_rooms': []}}
# --------------------
# {'school': {'room1': {'student1': 'Mario', 'student2': 'Paulo', 'student3': 'Bernd', 'student4': 'Richard', 'student5': 'Mairo', 'student6': 'Antonio'}, 'room2': {}, 'room3': {'student1': 'Bruno'}}, 'university': {'all_rooms': [1, 2, 3]}}
# <class '__main__.PunktDict'>
# <class 'dict'>

```