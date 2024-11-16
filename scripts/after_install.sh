#!/usr/bin/env bash

# kill any servers that may be running in the background 
sudo pkill -f runserver

# kill frontend servers if you are deploying any frontend
# sudo pkill -f tailwind
# sudo pkill -f node

sudo chmod -R 777 ./django-aws_cicd/

cd /home/ubuntu/django-aws_cicd/

# activate virtual environment
sudo python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
#pip install -r /home/ubuntu/django-aws_cicd/requirements.txt

# run server
cd altius
python3 manage.py runserver 0:8000 
