import tweepy
import json
import pymongo

import string
import wget
import os

import argparse
import io
from google.cloud import vision
from google.cloud.vision import types


consumer_key = 	'X'
consumer_secret = 'X'

access_token = 'X'
access_token_secret = 'X'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

def q_search(item):		

	connection = pymongo.MongoClient("mongodb://localhost")
	db = connection.twitter
	record = db.twitter_collection

	public_tweets = api.search( str(item) , count = 15)		#change the count if you want to search for more items

	for tweet in public_tweets:		#Searching through tweets generated

		print(tweet.text)

def quick_search(item, directory):		

	public_tweets = api.search( str(item) , count = 15)		#change the count if you want to search for more items

	media_files = set()		#Using a set since sets can't contain duplicate items, so I dont have duplicate photos

	for tweet in public_tweets:		#Searching through tweets generated

		media_item = tweet.entities.get('media', [])	#Getting multimedia content of tweet

		print(tweet.text)

		if len( media_item ) > 0 :	#Checking if there are any multimedia content within a tweet

			media_files.add(media_item[0]['media_url'])	#found multimedia content will be added to the set

	if( len(media_files) == 0):		#Case in which no tweets with multimedia content were found
		new_item = raw_input("Sorry, your search yielded no pictures.\n Please enter a new search query. \n")
		quick_search(new_item, directory)
			
	for media in media_files:	#iterating through set of images
		
		#downloading images via url, and storing into folder in directory called 'twitter_images'
		s = wget.download(media,out = str(directory))

	print(media_files)

	return media_files

#Function that retrieves facial sentiment analysis and web entities from a photo in a directory, and returns 
# a dictionary with the key being the path to the photo and value being the data from Google Cloud Vision API
def detect_faces_and_web(path):		
    
    client = vision.ImageAnnotatorClient()

    # [START migration_face_detection]
    # [START migration_image_file]
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)
    # [END migration_image_file]

    response = client.face_detection(image=image)		#face detection
    faces = response.face_annotations

    response2 = client.web_detection(image=image)       #web detection
    notes = response2.web_detection

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')

    ideal_likelihoods = ['POSSIBLE','LIKELY', 'VERY_LIKELY']

    photo_label = {}	#dictionary value that will have the label paired with its image, and will be returned

    added = False  #flag for checking if an item was added to the dictionary

     
    temp = {}

    vals = []

    #Here we are printing the web entities found from the photo
    if notes.web_entities:
        print ("{} Web entities found: ".format( len(notes.web_entities) ))
        for val in notes.web_entities:
            print('Score      : {}'.format( val.score ) )
            print('Description: {}'.format( (val.description).encode('ascii','replace') ) )
            vals.append('Description: {}'.format( (val.description).encode('ascii','replace') ) )

            temp = {path: vals}

            photo_label.update(temp)
            

    #Here we are doing the facial sentiment analysis appending a sentiment value to our list
    # which we then update our return dictionary variable with
    for face in faces:

    	print("Figuring out facial sentiment in photos. \n")

    	print("current image " + path + "\n")

    	if ( likelihood_name[face.anger_likelihood] in ideal_likelihoods ):
    		print('anger: {}'.format(likelihood_name[face.anger_likelihood]))

    		vals.append("anger: {}".format(likelihood_name[face.anger_likelihood]))

    		temp = {path: vals}

    		#adds temporary dictionary variable to the main dictionary
    		photo_label.update(temp)

    	if ( likelihood_name[face.joy_likelihood] in ideal_likelihoods ):
    		print('joy: {}'.format(likelihood_name[face.joy_likelihood]))

    		vals.append("joy: {}".format(likelihood_name[face.joy_likelihood]))

    		temp = {path: vals}

    		#adds temporary dictionary variable to the main dictionary
    		photo_label.update(temp)

    	if ( likelihood_name[face.surprise_likelihood] in ideal_likelihoods):
    		print('surprise: {}'.format(likelihood_name[face.surprise_likelihood]))

    		vals.append("surprise: {}".format(likelihood_name[face.surprise_likelihood]))

    		temp = {path: vals}

    		#adds temporary dictionary variable to the main dictionary
    		photo_label.update(temp)

    	added = True

    #This case is for if the facial analysis didn't return any values from our ideal_likelihoods list
    if added == False:
    	print('unsure emotions')

    	vals.append("unsure emotions")

    	temp = {path: vals}

    	photo_label.update(temp)

    #This case is for if the facial analysis failed to work at all
    if ( len(vals) == len(notes.web_entities) ):
    	print('did not work')
    	vals.append("did not work")

    	temp = {path: vals}

    	photo_label.update(temp)



    #print("\n")

    #print(vals)

    #print(photo_label)

    return photo_label

#function which will run the Google Cloud Vision API to and image from a directory 
def run_api(file, directory):		
	
	dicto = {}

	for filename in os.listdir(directory):

		if filename.endswith(".jpg"): 

			if filename == file:

				print("Current File: " + filename + "\n")
				dicto.update(detect_faces_and_web(os.path.join(directory, filename)))

			continue
		else:
			continue

	print(dicto)
	return dicto

def main_run():

	connection = pymongo.MongoClient("mongodb://localhost")
	db = connection.twitter
	record = db.twitter_collection

	item = raw_input("Please input something you want to search.\n ")

	#Here we are running the Twitter script which downloads photos from a search
	quick_search( item, os.getcwd() )

	dicto = {}

	#Applying the google cloud vision to photos in the current directory
	for filename in os.listdir( os.getcwd() ):
		if filename.endswith(".jpg"):

			#record.insert( dicto, check_keys=False )

			dicto.update( run_api( filename, os.getcwd() ) )
			
			continue
		else:
			continue

	#Deleting all the photos in the directory
	for filename in os.listdir( os.getcwd() ):
		if filename.endswith(".jpg"):

			os.remove(filename)
			
			continue
		else:
			continue

	#Here we insert the dictionary object into the MongoDB database
	record.insert( dicto, check_keys=False )

	return dicto

final_dict = {}

final_dict = main_run()

print(final_dict)





