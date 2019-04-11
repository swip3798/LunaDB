[![License: LGPL v3](https://img.shields.io/badge/License-LGPL%20v3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)
[![Generic badge](https://img.shields.io/badge/Python%20Version-3.x-green.svg)]()
# LunaDB
LunaDB is a document oriented file based database written in Python. It's designed on similar scenarios as [TinyDB](https://github.com/msiemens/tinydb), but with a better scaling with more documents and (hopefully) less memory usage. 
## Introduction
LunaDB reads only one document at a time and doesn't save the whole database in one giant JSON. Instead it saves every document as an own JSON and seperates them by line breaks.  
Main features from LunaDB:
* Document based: Like TinyDB, you can store documents as `dict`
* Written in pure Python: LunaDB doesn't require any other dependency
* Even more tiny: LunaDB has less than 500 lines of code, without unittests  
Important: LunaDB stores the data in multiple files located in one folder!
## Supported Python Versions
LunaDB supports only Python 3, there is no Python 2 support and there won't be any. As it is using `os.replace()` it needs at least Python 3.3 to run. Newer versions should be no problem. I use this module on Windows 10 and Debian Strech, it should run on any OS, if not feel free to open an issue.

## Example Usage
```python
from LunaDB import LunaDB
db = LunaDB("relative/path/to/database")

# If you are not giving an specific field, which will be unique, an automatic id_field will be used
character = db.table("character")
city = db.table("city", id_field="name")

# If strict is True it will throw an error if there is duplicated entry. Otherwise it will just skip the entry.
character.insert({"name": "Tristan", "age": 21}, strict = True)
character.insert({"name": "Isolt", "age": 19}, strict = False)

# To insert multiple entries at once, use insert_multiple
city.insert_multiple([{"name":"London"}, {"name": "Manchester"}])
```
### Searching for entries
Searching works with filter functions. The search method takes a function which returns `True` when the entry should be in the response. This filter function can be defined seperatly or with the lambda statement.
```python
res = character.search(lambda entry: entry["age"] == 21)
# res = [{"name":"Tristan", "age": 21, "_id": 0}]
res = character.search(lambda entry: entry["age"] < 22)
# res = [{"name": "Tristan", "age": 21, "_id": 0}, {"Isolt", "age":19, "_id":1}]
# The "_id" field is the auto_increment identifier
res = city.search(lambda entry: entry["name"] == "London")
# res = [{"name": "London"}]
```
### Update
The update