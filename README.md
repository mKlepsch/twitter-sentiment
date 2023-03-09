# Tweet Collector

This project is a tweet collector that can collect tweets for a specific hashtag, perform ETL (extract, transform, load) jobs, and display the results on a customizable dashboard. The project is split into three parts: a tweet collector, an ETL job, and a dashboard. Each part is a separate Docker container and is orchestrated using Docker Compose.
# Overview

The tweet collector scrapes Twitter for tweets containing a specific hashtag and saves them to a MongoDB database. The ETL job then extracts data from the MongoDB database, performs sentiment analysis using Vader, and saves the results to a PostgreSQL database. Finally, the dashboard displays the data in a customizable format using Metabase.

The project is written in Python and utilizes several libraries such as Tweepy, VaderSentiment, PyMongo, and Psycopg2. The project is organized using Docker Compose, making it easy to deploy and manage the different parts of the project.

# Note
the docker compose needs a .env file with following lines  (change to your hearts content):
>	POSTGRES_USER='postgres'
>	POSTGRES_PASSWORD='postgres'
>	POSTGRES_DB='twitter_db'
>	MONGO_INITDB_ROOT_USERNAME='root'
>	MONGO_INITDB_ROOT_PASSWORD='example'
>	BEARER_TOKEN=YOUR_TWITTER_API_ACCESSKEY