import pymongo
import json

from bson import json_util

myclient = pymongo.MongoClient(
    "mongodb+srv://mocko:6NWUbYTKwVp37Pg@spotifystorage.opo7e.mongodb.net/test?authSource=admin&replicaSet=atlas-mzt6pf-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true")
mydb = myclient["spotifystorage"]
mycol = mydb["songs"]
testarr = {'data': []}

for x in mycol.find():
    testarr['data'].append(x)

x1 = json.loads(json_util.dumps(testarr))

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(x1, f, ensure_ascii=False)
