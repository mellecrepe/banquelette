FROM alpine

MAINTAINER Lertsenem <lertsenem@lertsenem.com>

RUN    apk update     \
    && apk add        \
           bash       \
           sed        \
           gcc        \
           git        \
           libc-dev   \
           python     \
           python-dev \
           py-pip     \
           sqlite

RUN    pip install      \
           django

RUN    mkdir /home/banquelette/

COPY   account       /home/banquelette/account
COPY   projet        /home/banquelette/projet
COPY   static        /home/banquelette/static
COPY   templates     /home/banquelette/templates
COPY   manage.py     /home/banquelette/manage.py
COPY   docker_run.sh /docker_run.sh

ENV    SECRET_KEY=""

EXPOSE 80

CMD [ "/docker_run.sh" ]
