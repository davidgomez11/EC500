import tweepy
import string

import wget

import argparse
import io

import os

from google.cloud import vision
from google.cloud.vision import types

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

import subprocess

import time

consumer_key = 	'XXXXXXX'
consumer_secret = 'XXXXXX'

access_token = 'XXXXXXX'
access_token_secret = 'XXXXXX'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


def image_search(item):		#Function which downloads images from a Twitter search


	public_tweets = api.search( str(item) , count = 100)

	media_files = set()		#Using a set since sets can't contain duplicate items, so I dont have duplicate photos

	for tweet in public_tweets:		#Searching through tweets generated

		media_item = tweet.entities.get('media', [])	#Getting multimedia content of tweet

		#print(tweet.text)

		if len( media_item ) > 0 :	#Checking if there are any multimedia content within a tweet

			media_files.add(media_item[0]['media_url'])	#found multimedia content will be added to the set

	if( len(media_files) == 0):		#Case in which no tweets with multimedia content were found
		new_item = raw_input("Sorry, your search yielded no pictures.\n Please enter a new search query. \n")
		image_search(new_item)
			

	for media in media_files:	#iterating through set of images
		wget.download(media,out = 'practice_photos')		#downloading images via url, and storing into folder called 'twitter_images'


def retrieve_images(directory):		#function which just prints out .jpg file names of a certain directory

	for filename in os.listdir(directory):
		if filename.endswith(".jpg"): 

			print(os.path.join(directory, filename))

			continue
		else:
			continue

def detect_faces(path):		#function which detects sentiment in faces from images
    
    client = vision.ImageAnnotatorClient()

    # [START migration_face_detection]
    # [START migration_image_file]
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)
    # [END migration_image_file]

    response = client.face_detection(image=image)
    faces = response.face_annotations

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')

    ideal_likelihoods = ['POSSIBLE','LIKELY', 'VERY_LIKELY']

    photo_label = {}	#dictionary value that will have the label paired with its image, and will be returned

    added = False  #flag for checking if an item was added to the dictionary

    s = str(path)

    photo_file = s[ (s.find('/') + 1): ]	#splices the path string to return just the name of the photo

    #print('Faces:')

    for face in faces:

    	#print("current image " + path)

    	if ( likelihood_name[face.anger_likelihood] in ideal_likelihoods ):
    		#print('anger: {}'.format(likelihood_name[face.anger_likelihood]))

    		#temporary dictionary variable which has the sentiment value paired with the image
    		temp = {path: "anger: {}".format(likelihood_name[face.anger_likelihood])}

    		#adds temporary dictionary variable to the main dictionary
    		photo_label.update(temp)

    	if ( likelihood_name[face.joy_likelihood] in ideal_likelihoods ):
    		#print('joy: {}'.format(likelihood_name[face.joy_likelihood]))

    		#temporary dictionary variable which has the sentiment value paired with the image
    		temp = {path: "joy: {}".format(likelihood_name[face.joy_likelihood])}

    		#adds temporary dictionary variable to the main dictionary
    		photo_label.update(temp)

    	if ( likelihood_name[face.surprise_likelihood] in ideal_likelihoods):
    		#print('surprise: {}'.format(likelihood_name[face.surprise_likelihood]))

    		#temporary dictionary variable which has the sentiment value paired with the image
    		temp = {path: "surprise: {}".format(likelihood_name[face.surprise_likelihood])}

    		#adds temporary dictionary variable to the main dictionary
    		photo_label.update(temp)

    	added = True

    	

    if added == False:
    	#print('unsure emotions')

    	temp = {path: "unsure emotions"}

    	photo_label.update(temp)

    return photo_label

def apply_funct(directory):		#function which will apply labels to images from a directory and create a video out of them

    dicto = {}	#Data structure which will contain the labels corresponding to their image

    for filename in os.listdir(directory):		
        if filename.endswith(".jpg"): 
            
            dicto.update(detect_faces(os.path.join(directory, filename)))
            time.sleep(2)

            continue
        else:
            continue
    
    print("in dictionary \n")

    for k,v in dicto.items():		#Adding labels to the images
        img = Image.open( os.path.abspath(k) )
        draw = ImageDraw.Draw(img)
        # font = ImageFont.truetype(<font-file>, <font-size>)
        font = ImageFont.truetype("arial.ttf", 20)
        # draw.text((x, y),"Sample Text",(r,g,b))
        draw.text((0, 0), str(v) ,(255,255,255),font=font)
        img.save(k)
        print(k,v)

	#The line below executes a ffmpeg command in the command line tool of which creates a video
	# out of the images in the current directory   
    fps = 1

    subprocess.call(["ffmpeg","-y","-r",str(fps),"-i", "%*.jpg","-vcodec","mpeg4", "-qscale","5", "-r", str(fps), "video5.avi"])


item = raw_input("Please input something you want to search.\n ")


image_search(item)

print("Running the rest of the operation. \n")

apply_funct(os.getcwd())	#applies function to current working directory