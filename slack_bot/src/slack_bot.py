import os
import requests
from sqlalchemy import create_engine
from dotenv import load_dotenv

sql = '''with tweets as (
            select DISTINCT ON (tweet) tweet,
                case when sentiment > 0 then 'positive'
                when sentiment <= 0 then 'negative'
                end as sentiment
            from sentimental_tweets
        )
        select
            sentiment,
            count(*) as anzahl_tweets,
            count(*)::float / (select count(*) from tweets) * 100 as prozentualer_anteil
        from tweets
        GROUP by sentiment'''

load_dotenv()
webhook_url = os.getenv('slack_webhook_url')
con_string = 'postgresql://postgres:postgres@postgres:5432/twitterdb'

engine = create_engine(con_string)


result = engine.execute(sql)
answers = []
for row in result:
    answers.append(row)

message = {'text': f'''
Hey guys. I am analyzing the responses to the lastest episode \
of _John Oliver's_ *Last Week Tonight*.

Since last Monday I have found {answers[0][1] + answers[1][1]} tweets.
From those {answers[0][1]} have a {answers[0][0]} sentiment. That makes {round(answers[0][2],2)}% of all tweets.
The remaining {answers[1][1]} ({round(answers[0][2],2)}%) tweets see the show in a {answers[1][0]} light.
'''}

requests.post(url=webhook_url, json=message)
