FROM python:2.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /opt/vpcode
WORKDIR /opt/vpcode
ADD requirements/*.txt /opt/vpcode/
RUN pip install -r dev_mysql.txt
# RUN pip install -r dev_postgres.txt
ADD . /opt/vpcode/
