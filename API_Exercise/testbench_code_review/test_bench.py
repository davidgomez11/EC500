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

from persons_main import *

 # Please change the * below to your twitter development access keys
consumer_key =  'X'
consumer_secret = 'X'

access_token = 'X'
access_secret = 'X'


#Test one
#Seeing if your code can take in numbers
input_val('123')

#Test two
input_val('Alex')

#Test three
#Simple test of a Twitter handle
input_val('neymarjr')

#Test four
#This test is for seeing if your code can take in unicode characters like ç 
input_val('Barça')


