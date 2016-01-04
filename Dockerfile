FROM python:2.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements/*.txt /code/
RUN pip install -r dev_mysql.txt
# RUN pip install -r dev_postgres.txt
ADD . /code/
