'''
1. EXTRACT the tweets from mongodb
- connect to the database 
- query the data
2. TRANSFORM the data
- clean the text before?
- sentiment analysis
- maybe transform data types?
3. LOAD the data into postgres
- connect to postgres 
- insert into postgres
'''
import logging 
import sys
import os
import pandas as pd
from pymongo import MongoClient
from sqlalchemy import create_engine
from time import sleep
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

### create connections to databases (check your mongosb and postgres in python notebooks (or luftdaten))
#get envirmental information - MONGO_INITDB_ROOT_USERNAME, MONGO_INITDB_ROOT_PASSWORD, BEARER_TOKEN
MONGO_USER = os.getenv('MONGO_INITDB_ROOT_USERNAME')
MONGO_PASSWORD = os.getenv('MONGO_INITDB_ROOT_PASSWORD')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
logging.warning("Loaded Secrets")
# log initial sleep so that data can be in the data base
sleep(15)

def extract() -> list[dict]:
    """extract tweets from mongodb
    """
    logging.warning("MongoDB connection establishing")
    uri = f'mongodb://{MONGO_USER}:{MONGO_PASSWORD}@mongodb:27017/'
    conn = MongoClient(uri)
    logging.warning("MongoDB connection established")
    db_connect_tries=0
    while db_connect_tries<3:
        try:
            db = conn.tweets_db
            logging.warning("MongoDB connection established and using tweets_db Database")
            break
        except:
            logging.error(f'Twitter Database tweets_db does not exist - Try {db_connect_tries} - waiting 3 Sec for new try ')
        if db_connect_tries == 3:
            logging.error('Twitter Database tweets_db does not exist')
            sys.exit('Twitter Database tweets_db does not exist')
        db_connect_tries+=1
        sleep(5)
    logging.info("MongoDB connection to tweets_db Database established")
    ## error handling when now tweets are in collection
    extracted_tweets = list(db.tweets.find())
    logging.info("MongoDB connection closed")
    conn.close()
    return extracted_tweets


def transform(extracted_tweets):
    ''' Transforms data: clean text, gets sentiment analysis from text, formats date '''
    ## sentiment analysis tomorrow, basically you pass text and get a number between 0-1 as the sentiment score
    ## add the sentiment to the tweet and store in a dataframe or a dictionary
    transformed_tweets = []
    logging.warning('Performing sentiment on tweets')
    for tweet in extracted_tweets:
        analyzer = SentimentIntensityAnalyzer()
        score = analyzer.polarity_scores(tweet['text'])
        # datatype of the tweet: dictionary
        tweet['sentiment'] = score.get('compound')  # adding a key: value pair with 'sentiment' as the key and the score as the value
        tweet['neg'] = score.get('neg')
        tweet['neu'] = score.get('neu')
        tweet['pos'] = score.get('pos')
        transformed_tweets.append(tweet)
        # transformed_tweets is a list of transformed dictionaries
    return transformed_tweets

def check_id(engine, id):
    output = engine.execute(f"SELECT * FROM tweets WHERE id = '{id}'").fetchall()
    return True if len(output) > 0 else False


def load(transformed_tweets):
    ''' Load final data into postgres'''
    pass
    uri = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@postgresdb:5432/{POSTGRES_DB}'
    logging.warning(uri)
    logging.warning('Postgres connection establishing')
    pg = create_engine(uri, echo=True)
    logging.warning('Postgres connection established')
    create_table ='''
        CREATE TABLE IF NOT EXISTS tweets (
        id BIGINT PRIMARY KEY,
        created_at TIMESTAMP,
        text VARCHAR(500),
        sentiment NUMERIC,
        neg FLOAT,
        neu FLOAT,
        pos FLOAT
        );
        '''
    logging.warning('Postgres creating table not not already exisiting')
    pg.execute(create_table)
    logging.warning('Loading data into Postgres')
    for tweet in transformed_tweets:
        id = tweet.get('id')
        df_keys=['id','created_at','text','sentiment','neg','neu','pos']

        logging.warning(tweet)
        df = pd.json_normalize(tweet, sep='_')#)
        if (check_id(pg,id)):
            logging.warning(f'Tweet with {id} already analysed')
        else:
            df[df_keys].to_sql(name="tweets",con=pg, if_exists='append', index=False)

def run_etl_job():
    logging.warning("Obtaining tweets from MongoDB")
    extract_tweets = extract()
    logging.warning("Performing sentiment analysis on tweets")
    transformed_tweets = transform(extract_tweets)
    logging.warning("Loadong analised tweets into Postgres")
    load(transformed_tweets)

if __name__ == '__main__':
    logging.warning('Starting ETL job')
    while True:
        run_etl_job()
        sleep(10)