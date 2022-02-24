FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /parser
COPY requirements.txt /parser/
RUN pip install -r requirements.txt
COPY parser parser/
