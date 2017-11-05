FROM python:3.5

MAINTAINER mellecrepe

ENV PYTHONUNBUFFERED 1
ENV ADMIN_PORT="${BANQUELETTE_PORT:-8000}"

RUN mkdir /home/banquelette

WORKDIR /home/banquelette

RUN apt-get update; \
    apt-get install -y bsdmainutils

ADD requirements.txt /home/banquelette/
RUN pip install -r requirements.txt
RUN rm requirements.txt
ADD . /home/banquelette/

RUN useradd -d /home/banquelette -m -s /bin/bash banquelette
RUN chown -R banquelette:banquelette /home/banquelette 

USER banquelette

EXPOSE $BANQUELETTE_PORT

CMD [ "/home/banquelette/docker_run.sh" "BANQUELETTE_PORT"]
