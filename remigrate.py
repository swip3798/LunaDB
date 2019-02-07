from LunaDB import LunaDB
from tinydb import TinyDB
import shutil
try:
    shutil.rmtree("new_trump_db")
except:
    pass

db = LunaDB("new_trump_db")
new_table = db.table("tweet", "id")

db = TinyDB("test.db")
table = db.table("tweet")

data = table.all()
print(len(data))

new_table.insert_multiple(data)
