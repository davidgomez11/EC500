import tweepy
import string

import wget

import argparse
import io

import os

from google.cloud import vision
from google.cloud.vision import types
from google.cloud import storage

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

import subprocess

import time

import datetime

consumer_key = 	'XXXXXXX'
consumer_secret = 'XXXXXX'

access_token = 'XXXXXXX'
access_token_secret = 'XXXXXX'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

#Function which downloads images from a Twitter search and stores them into a directory
def image_search(item, directory):		


	public_tweets = api.search( str(item) , count = 10)		#change the count if you want to search for more items

	media_files = set()		#Using a set since sets can't contain duplicate items, so I dont have duplicate photos

	for tweet in public_tweets:		#Searching through tweets generated

		media_item = tweet.entities.get('media', [])	#Getting multimedia content of tweet

		#print(tweet.text)

		if len( media_item ) > 0 :	#Checking if there are any multimedia content within a tweet

			media_files.add(media_item[0]['media_url'])	#found multimedia content will be added to the set

	if( len(media_files) == 0):		#Case in which no tweets with multimedia content were found
		new_item = raw_input("Sorry, your search yielded no pictures.\n Please enter a new search query. \n")
		image_search(new_item)
			
	i = 0
	for media in media_files:	#iterating through set of images
		
		#downloading images via url, and storing into folder in directory called 'twitter_images'
		s = wget.download(media,out = str(directory))

		print("\n")

		str_ver = str(media)

		photo_file = str_ver[ (str_ver.rfind('/') + 1): ]	#Looking for substring of photo in media string

		#print(media)

		#print(photo_file)

		#print("\n")


		#From here I rename the images to a certain pattern (i.e. "image-01.jp" or "image-11.jpg")
		# and I generate a black photo right after each image, to put labels onto later
		if i < 9:
			(os.rename(os.path.join( str(directory) , photo_file), os.path.join( str(directory) , "image-0{}.jpg".format(i))))

			i+=1

			img = Image.open( os.path.abspath("black_big_ver.jpg") )

			(img.save(os.path.abspath(str(directory)) + "/image-0{}.jpg".format(i), "JPEG"))
	
			i+=1

		else:
			(os.rename(os.path.join( str(directory) , photo_file), os.path.join( str(directory) , "image-{}.jpg".format(i))))

			i+=1

			img = Image.open( os.path.abspath("black_big_ver.jpg") )

			(img.save(os.path.abspath(str(directory)) + "/image-{}.jpg".format(i), "JPEG"))
	
			i+=1

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    """GOOGLE FUNCTION FROM https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/storage/cloud-client/snippets.py """
    """NOT MY PROPERTY"""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print('File {} uploaded to {}.'.format(
        source_file_name,
        destination_blob_name))


def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    """GOOGLE FUNCTION FROM https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/storage/cloud-client/snippets.py """
    """NOT MY PROPERTY"""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    blob.download_to_filename(destination_file_name)

    print('Blob {} downloaded to {}.'.format(
        source_blob_name,
        destination_file_name))

#Function which downloads all blobs from a bucket on Google Cloud Storage
def download_all_blobs(bucket_name):

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blobs = bucket.list_blobs()

    for blob in blobs:
    	#print(blob.name)

    	download_blob(bucket_name, blob.name, blob.name)

    	print('Blob {} downloaded to {}.'.format(blob.name, os.getcwd() ))

		

#Function which uploads .jpg files to a bucket in the Google Cloud Storage from a directory
def upload_all_to_gcloud(directory, bucket_name):
	for filename in os.listdir(directory):
		if filename.endswith(".jpg"): 

			upload_blob( str(bucket_name) , os.path.join(directory, filename), filename)
			
			continue
		else:
			continue

#Function which uploads a .jpg file to a bucket in the Google Cloud Storage from a directory
def upload_single_to_gcloud(directory, name, bucket_name):
	for filename in os.listdir(directory):
		if filename.endswith(".jpg"):
			
			if filename == name:	#finding correct file to upload

				upload_blob( str(bucket_name) , os.path.join(directory, filename), filename)
			
			continue
		else:
			continue


#Function that deletes .jpg files in a directory, except a file you want to skip (basically )
def delete_jpg(directory, skip):
	for filename in os.listdir(directory):
		if filename.endswith(".jpg"):

			if filename == skip:
				continue

			else:
				os.remove(filename)
			
			continue
		else:
			continue

#Function which downloads images from a Twitter search and uploads them to Google Cloud Storage,
# and deletes those images from your directory, since they are in the cloud
def image_search_cloud_ver(item, bucket_name, directory):		


	public_tweets = api.search( str(item) , count = 10)		#change the count if you want to search for more items

	#time.sleep(2)

	media_files = set()		#Using a set since sets can't contain duplicate items, so I dont have duplicate photos

	for tweet in public_tweets:		#Searching through tweets generated

		media_item = tweet.entities.get('media', [])	#Getting multimedia content of tweet

		#print(tweet.text)

		if len( media_item ) > 0 :	#Checking if there are any multimedia content within a tweet

			media_files.add(media_item[0]['media_url'])	#found multimedia content will be added to the set

	if( len(media_files) == 0):		#Case in which no tweets with multimedia content were found
		new_item = raw_input("Sorry, your search yielded no pictures.\n Please enter a new search query. \n")
		image_search(new_item)
			
	i = 0
	for media in media_files:	#iterating through set of images
		
		#downloading images via url, and storing into folder into current working directory
		wget.download(media,out = str(os.getcwd()) )

		str_ver = str(media)

		photo_file = str_ver[ (str_ver.rfind('/') + 1): ]	#Looking for substring of photo in media string

		image1 = ""
		image2 = ""

		#From here I rename the images to a certain pattern (i.e. "image-01.jp" or "image-11.jpg")
		# and I generate a black photo right after each image, to put labels onto later
		if i < 9:
			(os.rename(os.path.join( str(directory) , photo_file), os.path.join( str(directory) , "image-0{}.jpg".format(i))))

			image1 = "image-0{}.jpg".format(i)

			i+=1

			img = Image.open( os.path.abspath("black_big_ver.jpg") )

			(img.save(os.path.abspath(str(directory)) + "/image-0{}.jpg".format(i), "JPEG"))

			image2 = "image-0{}.jpg".format(i)
	
			i+=1

		else:
			(os.rename(os.path.join( str(directory) , photo_file), os.path.join( str(directory) , "image-{}.jpg".format(i))))

			image1 = "image-0{}.jpg".format(i)

			i+=1

			img = Image.open( os.path.abspath("black_big_ver.jpg") )

			(img.save(os.path.abspath(str(directory)) + "/image-{}.jpg".format(i), "JPEG"))

			image2 = "image-0{}.jpg".format(i)
	
			i+=1

		time.sleep(2)

		#Uploads two generated photos to the cloud
		upload_single_to_gcloud( str(os.getcwd()), image1,  bucket_name )
		upload_single_to_gcloud( str(os.getcwd()), image2,  bucket_name )

	#Runs delete function on current working directory to delete .jpg files in your cwd, except black_big_ver.jpg
	delete_jpg( os.getcwd(), "black_big_ver.jpg" )	


#function which just prints out .jpg file names of a certain directory
def retrieve_images(directory):		

	for filename in os.listdir(directory):
		if filename.endswith(".jpg"): 

			print(os.path.join(directory, filename))

			continue
		else:
			continue
#function that renames .jpg files to (image-0, image-1) format of a certain directory, probably need to update this function
def rename_images(directory):		
	
	i = 0

	for filename in os.listdir(directory):
		if filename.endswith(".jpg"): 

			os.rename(os.path.join(directory, filename), os.path.join(directory, "image-{}.jpg".format(i)))
			
			i+=1

			continue
		else:
			continue

#function which detects sentiment in faces from images as well as their top 3 web entities
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

    time.sleep(2)

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')

    ideal_likelihoods = ['POSSIBLE','LIKELY', 'VERY_LIKELY']

    photo_label = {}	#dictionary value that will have the label paired with its image, and will be returned

    added = False  #flag for checking if an item was added to the dictionary

    print("REGULAR: " + path + "\n")

    #The calculations below for incremented_file basically sets the key to the correct file, that being 
    # the incremented one so it can add a label as its value later on
    incremented_file = path[0:(path.find(".jpg")-1)] +  str(int(path[ (path.find(".jpg") - 1): (path.find(".jpg"))]) + 1) + path[path.find(".jpg"):]

    #Checking if the file is under the format of "image-11.jpg" so the calculation below does the correct calculation for 
    # the incremented_file variable
    if int(path[ (path.find(".jpg") - 2): (path.find(".jpg") - 1 )]) != 0:
        incremented_file = path[0:(path.find(".jpg")-2)] +  str(int(path[ (path.find(".jpg") - 2): (path.find(".jpg"))]) + 1) + path[path.find(".jpg"):]

    print("Incremented: " + incremented_file + "\n")

    #print('Faces:')

    print("FILE no: " + path[ (path.rfind('-')+ 1) : path.rfind('.') ] + "\n") 

    #checking if photo is even if not we skip it, because the odd photos are the black jpgs,
    # where the label will go onto from the previous photo
    if (int( path[ (path.rfind('-')+ 1) : path.rfind('.') ] ) % 2 == 0) : 
    	temp = {}

    	vals = []

    	#Here we are taking the top 3 web items found in the web entities for the image and 
    	# adding it to a list which we will append to later
        if notes.web_entities:
            #print ('\n{} Web entities found: '.format(len(notes.web_entities)))
            try:
            	ver1 = (notes.web_entities[0].description).encode('ascii','replace')
            	ver2 = (notes.web_entities[1].description).encode('ascii','replace')
            	ver3 = (notes.web_entities[2].description).encode('ascii','replace')
            	vals.append(ver1)
            	vals.append(ver2)
            	vals.append(ver3)
            except IndexError:
            	diff = 3 - len(vals)
            	if diff == 1:
            		vals.append("no value")
            	if diff == 2:
            		vals.append("no value")
            		vals.append("no value")

        if len(vals) == 0:
        	vals.append("no value")
        	vals.append("no value")
        	vals.append("no value")

        #Here we are doing the facial sentiment analysis appending a sentiment value to our list
        # which we then update our return dictionary variable with
    	for face in faces:

    		print("Figuring out facial sentiment in photos. \n")

    		#print("current image " + path)

    		if ( likelihood_name[face.anger_likelihood] in ideal_likelihoods ):
    			#print('anger: {}'.format(likelihood_name[face.anger_likelihood]))

    			print("HEREE 1 \n")

    			vals.append("anger: {}".format(likelihood_name[face.anger_likelihood]))

                temp = {incremented_file: vals}

                #adds temporary dictionary variable to the main dictionary
                photo_label.update(temp)

    		if ( likelihood_name[face.joy_likelihood] in ideal_likelihoods ):
    			#print('joy: {}'.format(likelihood_name[face.joy_likelihood]))

    			print("HEREE 2 \n")

    			vals.append("joy: {}".format(likelihood_name[face.joy_likelihood]))

                temp = {incremented_file: vals}

                #adds temporary dictionary variable to the main dictionary
                photo_label.update(temp)

    		if ( likelihood_name[face.surprise_likelihood] in ideal_likelihoods):
    			#print('surprise: {}'.format(likelihood_name[face.surprise_likelihood]))

    			print("HEREE 3 \n")

    			vals.append("surprise: {}".format(likelihood_name[face.surprise_likelihood]))

                temp = {incremented_file: vals}

                #adds temporary dictionary variable to the main dictionary
                photo_label.update(temp)

    		added = True

    	#This case is for if the facial analysis didn't return any values from our ideal_likelihoods list
    	if added == False:
    		#print('unsure emotions')

    		vals.append("unsure emotions")

    		temp = {incremented_file: vals}

    		photo_label.update(temp)

    else:
        print("skipping odd photo. \n")

    #This case is for if the facial analysis failed to return any value 
    if incremented_file in photo_label:
    	if len(photo_label[incremented_file]) == 3:		#checking length of list of items gathered from google 
    		photo_label[incremented_file].append("did not work")

    print(photo_label)

    return photo_label

#Function which detects faces and web entities in a file located in Google Cloud Storage and adds labels to them
def detect_faces_and_web_uri(uri, image_name, bucket_name):		
    
    client = vision.ImageAnnotatorClient()
    # [START migration_image_uri]
    image = types.Image()
    image.source.image_uri = uri
    # [END migration_image_uri]

    response = client.face_detection(image=image)
    faces = response.face_annotations

    response2 = client.web_detection(image=image)
    notes = response2.web_detection

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')

    ideal_likelihoods = ['POSSIBLE','LIKELY', 'VERY_LIKELY']

    photo_label = []

    added = False  #flag for checking if an item was added to the dictionary

    path = str(image_name)

    print("REGULAR: " + path + "\n")

    #The calculations below for incremented_file basically sets the key to the correct file, that being 
    # the incremented one so it can add a label as its value later on
    incremented_file = path[0:(path.find(".jpg")-1)] +  str(int(path[ (path.find(".jpg") - 1): (path.find(".jpg"))]) + 1) + path[path.find(".jpg"):]

    #Checking if the file is under the format of "image-11.jpg" so the calculation below does the correct calculation for 
    # the incremented_file variable
    if int(path[ (path.find(".jpg") - 2): (path.find(".jpg") - 1 )]) != 0:
        incremented_file = path[0:(path.find(".jpg")-2)] +  str(int(path[ (path.find(".jpg") - 2): (path.find(".jpg"))]) + 1) + path[path.find(".jpg"):]

    print("Incremented: " + incremented_file + "\n")

    print("FILE no: " + path[ (path.rfind('-')+ 1) : path.rfind('.') ] + "\n")
    #print('Faces:')

    img = None
    draw = None

    if (int( path[ (path.find('-')+ 2) ] ) % 2 == 0) : #checking if photo is even if not we skip it
    	#time.sleep(2)
    	vals = []

        if notes.web_entities:
            print ('\n{} Web entities found: '.format(len(notes.web_entities)))

            ver1 = (notes.web_entities[0].description).encode('ascii','replace')
            ver2 = (notes.web_entities[1].description).encode('ascii','replace')
            ver3 = (notes.web_entities[2].description).encode('ascii','replace')

            vals.append(ver1)
            vals.append(ver2)
            vals.append(ver3)
            #print vals

    	for face in faces:
    		print("Figuring out facial sentiment in photos. \n")

    		#print("current image " + path)

    		if ( likelihood_name[face.anger_likelihood] in ideal_likelihoods ):
    			#print('anger: {}'.format(likelihood_name[face.anger_likelihood]))

    			vals.append("anger: {}".format(likelihood_name[face.anger_likelihood]))

                photo_label = vals

    		if ( likelihood_name[face.joy_likelihood] in ideal_likelihoods ):
    			#print('joy: {}'.format(likelihood_name[face.joy_likelihood]))

    			vals.append("joy: {}".format(likelihood_name[face.joy_likelihood]))

                photo_label = vals

    		if ( likelihood_name[face.surprise_likelihood] in ideal_likelihoods):
    			#print('surprise: {}'.format(likelihood_name[face.surprise_likelihood]))

    			vals.append("surprise: {}".format(likelihood_name[face.surprise_likelihood]))

                photo_label = vals

    		added = True

        

    	if added == False:
    		print('unsure emotions')

    		#temp = "unsure emotions"

    		#photo_label += (temp)

    		vals.append("unsure emotions")

    		#temp = {incremented_file: vals}

    		photo_label = vals

    	#This case is for if the facial analysis failed to return any value 
    	if len(photo_label) == 3:		#checking length of list of items gathered from google 
    		photo_label.append("did not work")

    	#Here we download the image from Google Cloud Storage bucket
    	download_blob(bucket_name, incremented_file, incremented_file )		

    	#Apply a label to the current image
    	img = Image.open( os.path.abspath(incremented_file) )

    	draw = ImageDraw.Draw(img)

    	# font = ImageFont.truetype(<font-file>, <font-size>)
    	font = ImageFont.truetype("arial.ttf", 20)
    	# draw.text((x, y),"Sample Text",(r,g,b))
    	#draw.text((0, 0), photo_label ,(255,255,255),font=font)

    	width, height = (500,400)
    	text_x, text_y = draw.textsize( str( photo_label ) )

    	x = (width - text_x)/2
    	y = (height - text_y)/2

    	draw.text((x,y - 10), ( str(photo_label[0]) + ", " + str(photo_label[1]) + ", " ) ,(255,255,255),font=font)
    	draw.text((x,y + 10), ( str(photo_label[2]) + ", " + str(photo_label[3]) ) ,(255,255,255),font=font)

    	img.save( incremented_file )

    	upload_blob(bucket_name, incremented_file, incremented_file)		#Here we upload the new annotated image to the bucket

    else:
        print("skipping odd photo. \n")

    delete_jpg( os.getcwd(), "black_big_ver.jpg" )
    #return photo_label

def apply_funct(directory):		#function which will apply labels to images from a directory and create a video out of them

    dicto = {}	#Data structure which will contain the labels corresponding to their image

    for filename in os.listdir(directory):

    	if filename == "black_big_ver.jpg":
    		continue

        if filename.endswith(".jpg"): 

        	print("Current File: " + filename + "\n")
        	dicto.update(detect_faces_and_web(os.path.join(directory, filename)))
        	time.sleep(2)

        	continue
        else:
        	continue
    
    #print("in dictionary \n")

    for k,v in dicto.items():		#Adding labels to the images

    	print("Adding labels to images. \n")

        img = Image.open( os.path.abspath(k) )
        width, height = img.size   #getting size of image
        draw = ImageDraw.Draw(img)
        # font = ImageFont.truetype(<font-file>, <font-size>)
        font = ImageFont.truetype("arial.ttf", 20)
        
        width, height = (600,480)
        text_x, text_y = draw.textsize( str(v) )

        x = (width - text_x)/2
        y = (height - text_y)/2

        # draw.text((x, y),"Sample Text",(r,g,b))
        #.text((0, 0), str(v) ,(255,255,255),font=font)

        #draw.text((x,y), str(v) ,(255,255,255),font=font)

        draw.text((x,y - 10), ( str(v[0]) + ", " + str(v[1]) + ", " ) ,(255,255,255),font=font)

        draw.text((x,y + 10), ( str(v[2]) + ", " + str(v[3]) ) ,(255,255,255),font=font)

        img.save(k)
        print(k,v)

    #Steps here before we create the video is basically duplicating the last .jpg file because
    # it doesn't get included into the video for some reason, so my quick fix was duplicating it and
    # adding it to .jpgs in the directory

    dict_list = []
    for k in dicto.keys():
        dict_list.append(k)

    dict_list.sort()

    last_file = str( dict_list[ len(dict_list) - 1 ] )  #getting the last file

    img = Image.open( os.path.abspath(last_file) )      #opening it

    extra_file = last_file[0:(last_file.rfind('/')-last_file.find('.')-3)] + "image-{}.jpg".format( len(dicto) + 10 )

    img.save(extra_file, "JPEG")    #saving it as a new file, duplicating it

    print("Creating video out of labeled images. \n")

	#The line below executes a ffmpeg command in the command line tool of which creates a video
	# out of the images in the current directory   
    fps = 0.5

    subprocess.call(["ffmpeg","-y","-r",str(fps),"-i", "%*.jpg","-vcodec","mpeg4", "-qscale","5", "-r", str(fps), "video10.avi"])

    #for windows users execute this version
    #subprocess.call(["ffmpeg.exe","-y","-r",str(fps),"-i", "%*.jpg","-vcodec","mpeg4", "-qscale","5", "-r", str(fps), "video4.avi"])


'''
function which calls other function and then ends up compiling the newly annotated images 
to a video and downloads them to the current working directory
'''
def apply_funct_v2(bucket_name):	
	storage_client = storage.Client()
	bucket = storage_client.get_bucket(bucket_name)

	blobs = bucket.list_blobs()

	count = 0

	for blob in blobs:		#gathering blobs

		uri = "gs://{}/{}".format(bucket_name, blob.name)

		detect_faces_and_web_uri(uri, blob.name, bucket_name)	#applying detection function
		time.sleep(2)

		count += 1

	print("Main operation done. \n")

	download_all_blobs(bucket_name)		#downloading all images to create a video out of them

	#Steps here before we create the video is basically duplicating the last .jpg file because
    # it doesn't get included into the video for some reason, so my quick fix was duplicating it and
    # adding it to .jpgs in the directory

	img = Image.open( os.path.abspath("black_big_ver.jpg") )      #opening it

	extra_file = "image-{}.jpg".format( count + 10 )

	img.save(extra_file, "JPEG")    #saving it as a new file, duplicating it

	print("Creating video out of labeled images. \n")

	#The line below executes a ffmpeg command in the command line tool of which creates a video
	# out of the images in the current directory   
	fps = 0.5

	subprocess.call(["ffmpeg","-y","-r",str(fps),"-i", "%*.jpg","-vcodec","mpeg4", "-qscale","5", "-r", str(fps), "video5.avi"])

	#for windows users execute this version
	#subprocess.call(["ffmpeg.exe","-y","-r",str(fps),"-i", "%*.jpg","-vcodec","mpeg4", "-qscale","5", "-r", str(fps), "video4.avi"])



"""-------------------------Running----------------------------------"""

#item2 = raw_input("Please input something you want to search.\n ")

#image_search_cloud_ver(item2, "twitter_images", os.getcwd() )

#print("Running the rest of the cloud operation. \n")

#apply_funct_v2("twitter_images")

"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

#item = raw_input("Please input something you want to search.\n ")

#image_search(item, os.getcwd() )

#print("Running the rest of the regular operation. \n")

#apply_funct( os.getcwd() )	#applies function to current working directory


"""------------------------------------------------------------------"""

