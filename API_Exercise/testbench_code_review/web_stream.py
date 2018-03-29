import sys

import tweepy
import string
import wget
import os

#from twitter_search import quick_search

from persons_main import *

from uuid import uuid4
from werkzeug import secure_filename

from Naked.toolshed.shell import execute_js		#This library allows me to run a script that runs a node.js file

Upload_Folder = str(os.getcwd())
Allowed_Extensions = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'avi'])

from flask import Flask, render_template, request, redirect, url_for, send_from_directory
app = Flask(__name__)
app.config['Upload_Folder'] = Upload_Folder

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1] in Allowed_Extensions

@app.route("/")
def hello():
    return "Hello World!"

# sys is a packet, this function will tell you the current version of python youre currently running
# type localhost:3333/version and it prints version that you are running 
@app.route('/version', methods=['GET'])
def version():
	return sys.version

# Main page for which we take the search query for the Twitter search to work on
# and after that we post something, http://localhost:5000/main
@app.route('/main', methods=['GET'])
def get_search():
	return render_template('image.html')

# Function of which calls the node.js script which posts the generated video of Twitter images on localhost:5000
@app.route('/return', methods=['POST'])
def get_image():
	search_item = request.values['image']
	
	input_val(search_item)

	#return render_template("upload.html", image_name=filename)

	#Run persons stuff to create a video 

	execute_js('read_directory.js', 'out.mp4')

	#return send_from_directory( str(os.getcwd()) , "vide04.avi")
	

	

@app.route('/return/<filename>')
def send_image(filename):
	return send_from_directory( str(os.getcwd()) , 'DVCtGExXkAIKOwH.jpg')

if __name__ == "__main__":
    app.run()

#app.run(host='0.0.0.0', port=3333, debug=True)









































