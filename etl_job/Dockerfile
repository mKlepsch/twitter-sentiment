FROM python:3.11
WORKDIR /app
COPY requirements.txt /app
COPY etl.py /app
RUN pip install --trusted-host pypi.python.org -r requirements.txt
CMD ["python", "etl.py"]
