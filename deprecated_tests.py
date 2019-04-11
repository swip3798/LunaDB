from LunaDB import LunaDB

db = LunaDB("test")
table = db.table("delete_test")


table.insert({"iojsdoija":"jdaojdw"})
table.insert({"saoijdiowj":2})
table.delete(lambda x: x["_id"] == 0)
