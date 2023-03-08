import tweepy
import os
import logging
from time import sleep
from pymongo import MongoClient

#get envirmental information - MONGO_INITDB_ROOT_USERNAME, MONGO_INITDB_ROOT_PASSWORD, BEARER_TOKEN
BEARER_TOKEN = os.getenv('BEARER_TOKEN')
MONGO_USER = os.getenv('MONGO_INITDB_ROOT_USERNAME')
MONGO_PASSWORD = os.getenv('MONGO_INITDB_ROOT_PASSWORD')
logging.warning("Loaded Secrets")

sleep(10)

#check if BEARER_TOKEN is set
if not BEARER_TOKEN:
    logging.error('BEARER_TOKEN empty!')
if MONGO_USER == 'root':
    logging.warning('USING default user!')
client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    wait_on_rate_limit=True,
)
# - means NOT
search_query = "#berniesanders -is:retweet -is:reply -is:quote lang:en -has:links"

def get_tweets(search_query):
    # create a client
    client = tweepy.Client(
        bearer_token=BEARER_TOKEN,
        wait_on_rate_limit=True
        )
    logging.info("Twitter Client created")
    cursor = tweepy.Paginator(
        method=client.search_recent_tweets,
        query=search_query,
        tweet_fields=['id', 'author_id', 'created_at', 'public_metrics'],
        user_fields=['username']
    ).flatten(limit=100)
    logging.info("Tweets collected")
    return cursor

def tweets_to_mongo(tweets):
    # connect to local MongoDB
    logging.info("MongoDB connection establishing")
    uri = f'mongodb://{MONGO_USER}:{MONGO_PASSWORD}@mongodb:27017/'
    conn = MongoClient(uri)
    logging.info("MongoDB connection established")
    # creates database
    tweet_db = conn.tweets_db
    logging.info("MongoDB connection to tweets_db Database established")
    # inserts tweet data into mongodb
    logging.warning("Inserting data into database tweets_db")
    for tweet in tweets:
        #if db.collection.count_documents({ 'UserIDS': newID }, limit = 1) != 0:
        if tweet_db.tweets.collection.count_documents( {'id':  tweet['id']},limit = 1  ) == 0:
            tweet_db.tweets.insert_one(dict(tweet))
        else:
            logging.warning(f"Tweet ({tweet['id']}) already in database")
    logging.warning("MongoDB connection closed")
    conn.close()

def run_tweet_collector():
    logging.info("Starting twitter acquisition")
    tweets = get_tweets(search_query)
    tweets_to_mongo(tweets)

if __name__ == "__main__":
    logging.warning('Starting Twitter collector')
    while True:
        run_tweet_collector()
        sleep(10)