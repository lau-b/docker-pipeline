#! python3

import os
import tweepy
import pymongo
from dotenv import load_dotenv

load_dotenv()

auth = tweepy.OAuthHandler(os.getenv('consumer_key'), os.getenv('consumer_secret'))
auth.set_access_token(os.getenv('access_token'), os.getenv('access_token_secret'))

api = tweepy.API(auth)
cursor = tweepy.Cursor(
    api.search,
    q='marco rose',
    tweet_mode='extended',
    lang='de'
)

for status in cursor.items(10):
    print(status.user.screen_name, status.full_text)
