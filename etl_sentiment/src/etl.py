import pymongo
import pandas as pd
import logging
from sqlalchemy import create_engine
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='/log/etl.log', filemode='a'
)

con_string = 'postgresql://postgres:postgres@postgres:5432/twitterdb'
client = pymongo.MongoClient('mongodb://mongodb:27017/')
sent = SentimentIntensityAnalyzer()


logging.info('starting mongo query')
res = client.twitterdb.lwt2.find({}, {'display_name': 1, 'tweet_text': 1, '_id': 0} )

tweets = []
for doc in res:
    sentiment = sent.polarity_scores(doc['tweet_text'])
    tweets.append([
            doc['display_name'],
            doc['tweet_text'],
            sentiment['compound']
        ]
    )

df_tweets = pd.DataFrame(tweets, columns=['screen_name', 'tweet', 'sentiment'])
logging.info(f'fetched {len(df_tweets)} row from mongodb')

df_tweets.drop_duplicates(['screen_name', 'tweet'], inplace=True)
logging.info(f'after dropping duplicates, {(len(df_tweets))} lines will have to be written to db')


engine = create_engine(con_string)
try:
    df_tweets.to_sql(con=engine, name='sentimental_tweets', if_exists='replace')
    logging.info(f'{len(df_tweets)} lines written to database')
except:
    logging.error('no data written to postgres')
