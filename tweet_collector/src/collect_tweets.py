#! python3

import os
import tweepy
import pymongo
from dotenv import load_dotenv

# Setting up Twitter connection
load_dotenv()
auth = tweepy.OAuthHandler(os.getenv('consumer_key'), os.getenv('consumer_secret'))
auth.set_access_token(os.getenv('access_token'), os.getenv('access_token_secret'))
api = tweepy.API(auth)

# Setting up mongodb connection
client = pymongo.MongoClient('mongodb://mongodb:27017')
db = client.twitterdb

cursor = tweepy.Cursor(
    api.search,
    q='marco rose',
    tweet_mode='extended',
    lang='de'
)

for status in cursor.items():
    hashtags = status.entities['hashtags']
    screen_name = status.user.screen_name
    user_name = status.user.name
    try:
        tweet = status.retweeted_status.full_text
    except AttributeError:  # Not a Retweet
        tweet = status.full_text


    db.rosenkrieg.insert_one({
        'name': user_name,
        'display_name': screen_name,
        'tweet_text': tweet,
        'hashtags': hashtags
        })

