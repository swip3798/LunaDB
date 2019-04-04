[![License: LGPL v3](https://img.shields.io/badge/License-LGPL%20v3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)
[![Generic badge](https://img.shields.io/badge/Python%20Version-3.x-green.svg)]()
# LunaDB
LunaDB is a document oriented file based database written in Python. It's designed on similar scenarios as [TinyDB](https://github.com/msiemens/tinydb), but with a better scaling with more documents and (hopefully) less memory usage.  
## Introduction
LunaDB reads only one document at a time and doesn't save the whole database in one giant JSON. Instead it saves every document as an own JSON and seperates them by line breaks.