
from pymongo import MongoClient
import pprint
client = MongoClient('127.0.0.1:27017')
db = client['test']
q1=[doc for doc in db.houston.aggregate([{"$group":{ "_id":"$created.user", "count":{"$sum":1}}},
                                         {"$sort":{"count":-1}},
                                         {"$limit":10}])]
pprint.pprint(q1)




q2=[doc for doc in db.houston.aggregate([{"$group":{ "_id":"$type", "count":{"$sum":1}}},
                                         {"$sort":{"count":-1}},
                                         {"$skip":1},
                                         {"$limit":10}])]
pprint.pprint(q2)




q3=[doc for doc in db.houston.aggregate([{"$group":{ "_id":"$tiger:county", "count":{"$sum":1}}},
                                         {"$sort":{"count":-1}},
                                         {"$skip":1},
                                         {"$limit":10}])]
pprint.pprint(q3)



q4=[doc for doc in db.houston.aggregate([{"$group":{ "_id":"$maxspeed", "count":{"$sum":1}}},
                                         {"$sort":{"count":-1}},
                                         {"$skip":1},
                                         {"$limit":8}])]
pprint.pprint(q4)

