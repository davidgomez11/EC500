import argparse
import io

import os

from google.cloud import vision
from google.cloud.vision import types

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


run_api('input your file here', os.getcwd())

