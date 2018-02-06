import tweepy
import string
import wget
import os


consumer_key = 	'X'
consumer_secret = 'X'

access_token = 'X'
access_token_secret = 'X'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

#Function that runs a Twitter search, retrieves photos and downloads them to a directory, as well as returning
# the set that contains the images
def quick_search(item, directory):		

	public_tweets = api.search( str(item) , count = 10)		#change the count if you want to search for more items

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


