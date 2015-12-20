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
           py-pip

RUN    pip install      \
           "django<1.9" \
           "couchdbkit"

RUN    echo "Doing some ugly things because couchdbkit is no longer maintained" >&2    \
    && sed -i "24d" '/usr/lib/python2.7/site-packages/couchdbkit/ext/django/schema.py' \
    && sed -i "63d" '/usr/lib/python2.7/site-packages/couchdbkit/ext/django/schema.py'

RUN    mkdir /home/banquelette/

COPY   account       /home/banquelette/account
COPY   projet        /home/banquelette/projet
COPY   static        /home/banquelette/static
COPY   templates     /home/banquelette/templates
COPY   manage.py     /home/banquelette/manage.py
COPY   initdb.sh     /home/banquelette/initdb.sh
COPY   initdb_data   /home/banquelette/initdb_data
COPY   docker_run.sh /docker_run.sh

ENV COUCHDB_HOST="db:5984" \
    SECRET_KEY=""

EXPOSE 80

CMD [ "/docker_run.sh" ]
