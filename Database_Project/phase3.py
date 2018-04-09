import tweepy
import json
import pymongo


consumer_key = 	'X'
consumer_secret = 'X'

access_token = 'X'
access_token_secret = 'X'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

def run_stuff(user):

	
	tweets = api.user_timeline(screen_name=user,
                           count=200, include_rts=False,
                           exclude_replies=True)
    

	#tweets = api.search( user , count = 100)		#change the count if you want to search for more items

	#print(tweets)

	connection = pymongo.MongoClient("mongodb://localhost")
	db = connection.twimonitor
	record = db.twimonitor_collection

	for tweet in tweets:		#Searching through tweets generated

		print(tweet.text)
		print(tweet.created_at)
		print(tweet.user.name)
		print(tweet.user.screen_name)
		print(tweet.user.location)
		print(tweet.user.followers_count)
		print(tweet.user.verified)
		print(tweet.retweet_count)

		dicto = {
					"text" : tweet.text, 
					"created_at" : tweet.created_at,
					"name" : tweet.user.name,
					"screen_name" : tweet.user.screen_name,
					"location" : tweet.user.location,
					"followers_count" : tweet.user.followers_count,
					"verified" : tweet.user.verified,
					"retweet_count" : tweet.retweet_count
				}

		#Here we insert the dictionary object into the MongoDB database
		record.insert( dicto, check_keys=False )
		
		print("\n")

		return tweets

def continous_run(user):
	
	tweets = run_stuff(user)	

	last_id = tweets[-1].id

	while(True):
		other_tweets = api.user_timeline(screen_name=user,
                                count=200,
                                include_rts=False,
                                exclude_replies=True,
                                max_id=last_id-1)

		if( len(other_tweets) == 0):
			break
        else:
        	last_id = other_tweets[-1].id-1 

        	#connection = pymongo.MongoClient("mongodb://localhost")
        	#db = connection.twimonitor
        	#record = db.twimonitor_collection

        	for tweet in other_tweets:		#Searching through tweets generated
        		print(tweet.text)
        		print(tweet.created_at)
        		print(tweet.user.name)
        		print(tweet.user.screen_name)
        		print(tweet.user.location)
        		print(tweet.user.followers_count)
        		print(tweet.user.verified)
        		print(tweet.retweet_count)

        		dicto = {
        					"text" : tweet.text, 
        					"created_at" : tweet.created_at,
        					"name" : tweet.user.name,
        					"screen_name" : tweet.user.screen_name,
        					"location" : tweet.user.location,
        					"followers_count" : tweet.user.followers_count,
        					"verified" : tweet.user.verified,
        					"retweet_count" : tweet.retweet_count
        				}

        		#Here we insert the dictionary object into the MongoDB database
        		#record.insert( dicto, check_keys=False )

        		print("\n")	


    #return other_tweets


run_stuff("neymarjr")
#run_stuff("justinbieber")
#continous_run("neymarjr")

