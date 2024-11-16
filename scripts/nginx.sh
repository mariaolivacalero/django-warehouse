
#!/usr/bin/bash

sudo systemctl daemon-reload
sudo rm -f /etc/nginx/sites-enabled/default

sudo cp /home/ubuntu/djangowarehouse/nginx/nginx.conf /etc/nginx/sites-available/warehouse
sudo ln -s /etc/nginx/sites-available/warehouse /etc/nginx/sites-enabled/
#sudo ln -s /etc/nginx/sites-available/warehouse /etc/nginx/sites-enabled
#sudo nginx -t
sudo gpasswd -a www-data ubuntu
sudo systemctl restart nginx
