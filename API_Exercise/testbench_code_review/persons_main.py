import tweepy
from tweepy import OAuthHandler
import json
import wget

import os
from base64 import b64encode
from os import makedirs
from os.path import join, basename
from sys import argv
import requests

import io

import PIL
from PIL import Image, ImageDraw, ImageFont

#Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

 # Please change the * below to your twitter development access keys
consumer_key =  'X'
consumer_secret = 'X'

access_token = 'X'
access_secret = 'X'
 
@classmethod
def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status
 
# Status() is the data model for a tweet
tweepy.models.Status.first_parse = tweepy.models.Status.parse
tweepy.models.Status.parse = parse
# User() is the data model for a user profil
tweepy.models.User.first_parse = tweepy.models.User.parse
tweepy.models.User.parse = parse
# You need to do it for all the models you need
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)

def input_val(username):
    
    #username=input('Twitter Username:')

    tweets = api.user_timeline(screen_name=username,
                            count=200, include_rts=False,
                            exclude_replies=True)
    last_id = tweets[-1].id
 
    while (True):
        more_tweets = api.user_timeline(screen_name=username,
                                    count=200,
                                    include_rts=False,
                                    exclude_replies=True,
                                    max_id=last_id-1)
    # There are no more tweets
        if (len(more_tweets) == 0):
            break
        else:
            last_id = more_tweets[-1].id-1
            tweets = tweets + more_tweets

    media_files = set()
    for status in tweets:
        media = status.entities.get('media', [])
        if(len(media) > 0):
            media_files.add(media[0]['media_url'])
 
    for media_file in media_files:
        wget.download(media_file)


    counter = -1
    for item in media_files:
        if (counter < 200):
            counter = counter +1
            address = os.getcwd() + '/' + str(counter) + '.jpg'
            wget.download(item,address)

    

    #-------------------------------------------- Implementation of the google API and generate Labels-------------------------------

    #********************#
    #counter = 200
    #********************#

    counter_two = 0
    client = vision.ImageAnnotatorClient()

    for x in range(0, counter +1):
        try:
            counter_two += x 
            name = str(counter_two) + '.jpg'

            path = os.getcwd()
            with io.open(path + '/' + name, 'rb') as image_file:
                content = image_file.read();

            image = types.Image(content = content)

            response = client.label_detection(image=image)
            labels = response.label_annotations
    

            new = 'new' +str(counter_two)+'.jpg'
            image = Image.open(name)
            draw = ImageDraw.Draw(image)
            y_coordinate = 70
            for item in labels: 
                word = item.description

                y_coordinate += 10
                draw.text((200, y_coordinate), text = word, fill=(250,250,250))


            image.save(new)
            newcommand = "rm " +name;
            os.system(newcommand)
        except IOError:
            break


    #    Using ffmpeg

    os.system("ffmpeg -framerate .5 -pattern_type glob -i '*.jpg' out.mp4")