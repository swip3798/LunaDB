from LunaDB import LunaDB

db = LunaDB("test")
table = db.table("id_tests")


table.insert({"Hi":"oi2joidjoi", "joidajoi":1})
rows = [
    {"adijw":"djsaoi"}, {"djaoidjw": "djoiajdwoi"}
]
table.insert_multiple(rows)