from LunaDB import LunaDB

def no_retweets(row):
    return not "retweeted_status" in row

db = LunaDB("new_trump_db")
table = db.table("tweet", id_field="id")

data = table.all()

for idx, i in enumerate(data[:20]):
    print(idx)
    i["updated"] = True
    try:
        table.update(i, auto_clean=False)
    except Exception as e:
        raise e

table.clean()