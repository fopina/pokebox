ARG BASE=python:2.7.14-alpine3.6
FROM $BASE

#RUN [ "cross-build-start" ]  # hub_arm_hack

RUN apk add --no-cache s6 nginx nmap

#RUN apk add --no-cache python2  # hub_arm_hack
#RUN python -m ensurepip  # hub_arm_hack

ADD pokebox/requirements.txt /var/app/requirements.txt
RUN pip install -r /var/app/requirements.txt
RUN pip install gunicorn

ADD docker/s6 /etc/s6
ADD docker/start.sh /start.sh
ADD docker/nginx.conf /etc/nginx/nginx.conf
ADD docker/crontab /etc/crontabs/root

RUN mkdir -p /run/nginx/

ADD pokebox /var/app

ADD docker/extra_settings.py /var/app/extra_settings
RUN cat /var/app/extra_settings >> /var/app/pokebox/settings.py

RUN python /var/app/manage.py collectstatic --noinput

#RUN [ "cross-build-end" ]  # hub_arm_hack

VOLUME /var/dbdata
EXPOSE 8080

CMD "/start.sh"
