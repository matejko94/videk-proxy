import json
import pymongo
from pymongo import MongoClient

class ProxyDatabase:
	client = MongoClient()
	db = client.proxy

	def __init__(self, collection):
		self.collection = self.db[collection]
		self.counter_id = collection + "_id"

		self.counter = self.db.counters.find_one({"_id":self.counter_id})
		if self.counter == None:
			self.db.counters.insert({'_id': self.counter_id, 'seq': 0})

	def getNextSequence(self, collection, name):
		return collection.find_and_modify(query= { '_id': name }, \
			update= { '$inc': {'seq': 1}}, new=True ).get('seq') - 1

	def store(self, description):
		db_id = self.collection.find_one(description)
		if db_id == None:
			description["_id"] = self.getNextSequence(self.db.counters, \
				self.counter_id)
			db_id = self.collection.insert_one(description).inserted_id
		else:
			db_id = db_id.get("_id")
		return db_id

	def get(self, db_id):
		return json.dumps(self.collection.find_one({"_id":int(db_id)}, \
			{"_id":False}))
