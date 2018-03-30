'''
Import airport location data and parse through it
Demonstrate Read Data, Update Data, and Search/Find Data
'''


import json
import pymongo

connection = pymongo.MongoClient("mongodb://localhost")
db = connection.book
record = db.book_collection

#Run these lines once to import the json file into a collection on your db
'''
page = open("airports.json", 'r')
parsed = json.loads(page.read())

for item in parsed:
    record.insert(item)
'''

#This line is doing a similar query to db.book_collection.find( { "city" : "Colorado", "name" : "Barra Colorado Airport" } )
# on the shell
for item in record.find({ "city" : "Colorado"}):
	print(item)

	#This line writes item to a txt file
	with open('data.txt', 'a') as the_file:
		the_file.write(str(item) + '\n')

	#The lines below looks for a cetain item in the collection and updates one of its values
	'''
	if str(item['_id']) == '5abbd0107c69021262834f83':
		print(item)
		record.update_one( { '_id' : item['_id'] } , { '$set' : { 'name' : "blah airport"} }, upsert=False )
		print(item)
	'''

#This line inserts an item into the db
#record.insert( {"test":"random"} )

#Shell Commands
'''
db.book_collection.find( { "city" : "Colorado" } )

db.book_collection.find( { "city" : "Colorado", "name" : "Barra Colorado Airport" } )
'''

