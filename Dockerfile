FROM ubuntu:12.10
MAINTAINER Alex Brandt <alunduil@alunduil.com>

RUN apt-get update
RUN apt-get upgrade -y

RUN apt-get install python-pip

ADD . /usr/local/src/margarine

RUN cd /usr/local/src/margarine
RUN pip install -r requirements.txt
RUN python setup.py install

USER margarine
EXPOSE 5000

ENTRYPOINT [ "/usr/bin/margarine" ]
CMD [ "tinge", "blend", "spread" ]
