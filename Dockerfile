FROM python:3.7.12-slim-buster

WORKDIR /app

RUN apt-get update && \ 
    apt-get install -y gcc g++ && \
    apt-get -y upgrade && \
    apt-get install -y ffmpeg

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app

CMD ["python", "main.py"]

