from LunaDB import LunaDB
import shutil

try:
    shutil.rmtree("test1")
except:
    pass


db = LunaDB("test1")
table = db.table("test", "id")
row = {
    "id": 99999,
    "name": "Christian",
    "age": 21
}
rows = []
table.insert(row)
for i in range(600):
    row = {
        "id": i,
        "name": "Christian",
        "age": 21
    }
    rows.append(row)
table.insert_multiple(rows)
res = table.search(lambda x: x["id"] == 300)
print(res)
table.delete(lambda x: x["id"] == 1)
table.delete(lambda x: x["id"] == 3)
table.delete(lambda x: x["id"] == 5)
table.delete(lambda x: x["id"] == 6)
table.delete(lambda x: x["id"] == 9)
table.delete(lambda x: x["id"] == 14)
res = table.search(lambda x: x["id"] == 1)
print(res)

table.update(row = {
        "id": 4,
        "name": "Updated",
        "age": 21
    })
res = table.search(lambda x: x["id"] == 4)
print(res)

table.upsert(row = {
        "id": 4,
        "name": "Updates",
        "age": 21
    })
res = table.search(lambda x: x["id"] == 4)
print(res)