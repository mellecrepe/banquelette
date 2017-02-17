FROM python:2.7

MAINTAINER mellecrepe

ENV PYTHONUNBUFFERED 1

RUN mkdir /home/banquelette

WORKDIR /home/banquelette

RUN apt-get update; \
    apt-get install -y bsdmainutils

ADD requirements.txt /home/banquelette/
RUN pip install -r requirements.txt
ADD . /home/banquelette/

RUN useradd -d /home/banquelette -m -s /bin/bash banquelette
RUN chown -R banquelette:banquelette /home/banquelette 

USER banquelette

CMD [ "/home/banquelette/docker_run.sh" ]
