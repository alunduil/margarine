FROM ubuntu:12.10
MAINTAINER Alex Brandt <alunduil@alunduil.com>

RUN apt-get update
RUN apt-get upgrade -y -qq

RUN apt-get install -y -qq python-pip

ADD . /usr/local/src/margarine
WORKDIR /usr/local/src/margarine

RUN mv setup.cfg setup.cfg.bak
RUN pip install -q -r requirements.txt
RUN mv setup.cfg.bak setup.cfg

RUN python setup.py install

RUN useradd -c 'added by docker for margarine' -d /usr/local/src/margarine -r margarine
USER margarine

EXPOSE 5000

ENTRYPOINT [ "/usr/local/bin/margarine" ]
CMD [ "tinge", "blend", "spread" ]
