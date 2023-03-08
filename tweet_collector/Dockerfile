FROM python:3.11
WORKDIR /app
COPY requirements.txt /app
COPY get_tweets.py /app
RUN pip install --trusted-host pypi.python.org -r requirements.txt
CMD ["python", "get_tweets.py"]
