import json
import sqlite3


#Load the json into a variable
airport_info = json.load(open("airports.json"))

#Open up a new sqlite database
db = sqlite3.connect("airport_json.db")

#Creating a cursor to execute SQL commands with
c = db.cursor()

#SQL command to create the table
query1 = '''CREATE TABLE air_table ( {0} {1} )'''

#Variable that holds all the keys of a dictionary object in the json file 
# which is used to create the correct columns in the database
columns = airport_info[0].keys()

#Inserting in the right elements into the query
query1 = query1.format( " text, ".join(columns), "text" )


#print(query1)

c.execute(query1)

db.commit()

#Iterating through the json file
for item in airport_info:

	#Lists which will hold the necessary keys and values which will eventually 
	# be inserted into the INSERT SQL command
	column_list = []
	row_list = []

	#Iterating through the keys and values of a single dictionary object in the json file
	for key, val in item.items():
		try:

			#Appending the key
			column_list.append(key.encode('utf-8'))

			string_val = ' "{}" '
			string_val = string_val.format(val.encode('utf-8'))

			#Appending the value
			row_list.append(string_val)

		except AttributeError:

			string_val = ' "{}" '
			string_val = string_val.format("null")

			#Appending the value
			row_list.append(string_val)

	#Creating the INSERT SQL command and formatting it with the concatenated column
	# and row lists 
	query3 = '''INSERT INTO air_table ( {0} ) VALUES ( {1} )'''
	query3 = query3.format( ' , '.join(column_list), ' , '.join(row_list) )
	#print(query3)
	
	c.execute(query3)
	db.commit()


#Commands here fetch all the data from the table and print it out
c.execute('''SELECT * FROM air_table''')
print(c.fetchall())
db.commit()
c.close()


