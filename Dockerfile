from ubuntu:12.10
maintainer Nick Stinemates

run apt-get update
run apt-get install -y python-setuptools
run easy_install pip
add . /website
run pip install -r /website/requirements.txt
env PYTHONPATH /website

expose 5000
expose 5050

