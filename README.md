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
The update uses the id field to identify the document and will replace it.
```python
res = character.search(lambda entry: entry["name"] == "Tristan")
# res = [{"name":"Tristan", "age": 21, "_id": 0}]
res["age"] = 22
character.update(res, auto_clean = True)
res = character.search(lambda entry: entry["name"] == "Tristan")
# res = [{"name":"Tristan", "age": 22, "_id": 0}]
```
The `auto_clean` parameter is present in every method that modifies or deletes existing data. Without auto_clean LunaDB does not delete the data from the database, in fact it is just disabling them. Only if the database is cleaned afterwards, the disabled entries will get deleted. If `auto_clean` is `False` you need to clean the table with the `table.clean()` method manually if you want to save space. If `auto_clean` is `True`, the table will automatically cleared when the disabled lines exceed the `auto_clean_buffer`, which is per default 5MB per table. `auto_clean_buffer` can be set with the creation of the database object. Per default `auto_clean` is `True`. 
### Delete
The delete works the same way as search, every row which returns at the filter function `True` will be deleted. The `auto_clean` is the same as with update.
```python
res = character.search(lambda entry: entry["name"] == "Tristan")
# res = [{"name":"Tristan", "age": 21, "_id": 0}]
character.delete(lambda entry: entry["name"] == "Tristan", auto_clean = True)
res = character.search(lambda entry: entry["name"] == "Tristan")
# res = []
```
### Additional concepts
#### Insert or update
```python
row = {"name":"Tristan", "age": 17}
character.upsert(row)
```
#### Insert or skip
```python
row = {"name":"Tristan", "age": 17}
# With strict = False, duplicated entries won't throw an exception
character.insert(row, strict = False)
```

## Additional documentation
Look at the [module reference](https://github.com/swip3798/LunaDB/blob/Add-documentation/docs/REFERENCE.md).

