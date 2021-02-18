import pymongo
from sqlalchemy import create_engine

con_string = 'postgresql://etlpipe:postgres@postgres:5432/twitterdb'

client = pymongo.MongoClient('mongodb://mongodb:27017/')
res = client.twitterdb.lwt2.find({}, {'display_name': 1, 'tweet_text': 1, '_id': 0} )

for doc in res:
    print(doc)


engine = create_engine(con_string)
