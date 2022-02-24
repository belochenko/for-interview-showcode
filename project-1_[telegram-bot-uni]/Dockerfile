FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /tg-bot
COPY requirements.txt /tg-bot/
RUN pip install -r requirements.txt
COPY . /tg-bot/