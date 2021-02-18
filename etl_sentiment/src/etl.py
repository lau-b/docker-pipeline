import pymongo
import pandas as pd
from sqlalchemy import create_engine
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


con_string = 'postgresql://postgres:postgres@postgres:5432/twitterdb'

client = pymongo.MongoClient('mongodb://mongodb:27017/')
res = client.twitterdb.lwt2.find({}, {'display_name': 1, 'tweet_text': 1, '_id': 0} )

sent = SentimentIntensityAnalyzer()

tweets = []
for doc in res:

    sentiment = sent.polarity_scores(doc['tweet_text'])
    tweets.append([
            doc['display_name'],
            doc['tweet_text'],
            sentiment['compound']
        ]
    )


df = pd.DataFrame(tweets, columns=['screen_name', 'tweet', 'sentiment'])
print(df)


engine = create_engine(con_string)
df.to_sql(con=engine, name='sentimental_tweets', if_exists='replace')

