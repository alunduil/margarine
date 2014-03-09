FROM ubuntu:12.10
MAINTAINER Alex Brandt <alunduil@alunduil.com>

RUN apt-get update
RUN apt-get upgrade -y -qq

RUN apt-get install -y -qq python-pip

ADD . /usr/local/src/margarine

RUN mv /usr/local/src/margarine/setup.cfg /usr/local/src/margarine/setup.cfg.bak
RUN cd /usr/local/src/margarine && pip install -q -r requirements.txt
RUN mv /usr/local/src/margarine/setup.cfg.bak /usr/local/src/margarine/setup.cfg

RUN cd /usr/local/src/margarine && python setup.py install

RUN useradd -c 'added by docker for margarine' -d /usr/local/src/margarine -r margarine
USER margarine

EXPOSE 5000

ENTRYPOINT [ "/usr/bin/margarine" ]
CMD [ "tinge", "blend", "spread" ]
