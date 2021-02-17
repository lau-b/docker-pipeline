import pymongo


client = pymongo.MongoClient('mongodb://mongodb:27017/')
res = client.twitterdb.lwt2.find({}, {'display_name': 1, 'tweet_text': 1, '_id': 0} )

for doc in res:
    print(doc)
