#!/usr/bin/env bash

# kill any servers that may be running in the background 
sudo pkill -f runserver

sudo chmod -R 777 ./django-aws_cicd/

cd /home/ubuntu/django-aws_cicd/

# activate virtual environment
sudo python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt


# Create or overwrite the Supervisor configuration file
sudo tee /etc/supervisor/conf.d/django_app.conf > /dev/null << EOL
[program:django_app]
command=/home/ubuntu/django-aws_cicd/venv/bin/python /home/ubuntu/django-aws_cicd/altius/manage.py runserver 0:8000
directory=/home/ubuntu/django-aws_cicd/altius
user=ubuntu
autostart=true
autorestart=true
stderr_logfile=/var/log/django_app.err.log
stdout_logfile=/var/log/django_app.out.log
EOL

# set environment variable onEc2 to true
sudo echo "export ON_EC2=true" >> /home/ubuntu/.bashrc

cd altius
python manage.py makemigrations
python manage.py migrate

# Reload Supervisor configuration and restart the app
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl restart django_app

# Exit successfully