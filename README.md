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
LunaDB supports only Python 3, there is no Python 2 support. Python 2 is dying anyway and shouldn't be used.

## Example Usage
```python
from LunaDB import LunaDB
db = LunaDB("relative/path/to/database")
table = db.table("example_table", id_field = "id")
```
The best way to use LunaDB is with tables. 