import os
import logging
import tweepy
import pymongo
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='/log/tweet_collector.log', filemode='a'
)
logging.info('Tweet Collector started.')
# Setting up Twitter connection
load_dotenv()
auth = tweepy.OAuthHandler(os.getenv('consumer_key'), os.getenv('consumer_secret'))
auth.set_access_token(os.getenv('access_token'), os.getenv('access_token_secret'))
api = tweepy.API(auth, wait_on_rate_limit=True)

# Setting up mongodb connection
client = pymongo.MongoClient('mongodb://mongodb:27017/')
db = client.twitterdb
logging.info('Connection successfully set up')

# Searching Twitter
cursor = tweepy.Cursor(
    api.search,
    q='LastWeekTonight',
    tweet_mode='extended',
    lang='en'
)

# Writing to mongodb
for status in cursor.items():
    # Maybe build a list of dictionaries and use insert_many()
    hashtags = status.entities['hashtags']
    screen_name = status.user.screen_name
    user_name = status.user.name
    try:
        tweet = status.retweeted_status.full_text
    except AttributeError:  # Not a Retweet
        tweet = status.full_text

    db.lwt2.insert_one(
        {'name': user_name,
         'display_name': screen_name,
         'tweet_text': tweet,
         'hashtags': hashtags}
    )
logging.info('Tweet Collector finished.')
