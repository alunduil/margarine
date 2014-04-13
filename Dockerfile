FROM ubuntu:13.10
MAINTAINER Alex Brandt <alunduil@alunduil.com>

RUN apt-get update
RUN apt-get upgrade -y -qq
RUN apt-get install -y -qq python-pip build-essential python-dev
RUN apt-get install -y -qq rsyslog

RUN useradd -c 'added by docker for margarine' -d /usr/local/src/margarine -r margarine
RUN ln -snf /usr/local/src/margarine/conf /etc/margarine

ADD . /usr/local/src/margarine

RUN pip install -q -e /usr/local/src/margarine

USER margarine
EXPOSE 5000

ENTRYPOINT [ "/usr/local/bin/margarine" ]
CMD [ "tinge", "blend", "spread" ]
