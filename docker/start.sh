#!/bin/sh

python /var/app/manage.py migrate
s6-svscan /etc/s6
