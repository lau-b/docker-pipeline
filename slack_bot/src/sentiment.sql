with tweets as (
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
GROUP by sentiment
;
