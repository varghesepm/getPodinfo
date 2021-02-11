FROM alpine:3.12

LABEL Maintainer="Varghese P Mathew <varghesepoyyali@gmail.com>"

RUN apk update \
    && apk add --no-cache python3 py3-pip python3-dev bash nginx supervisor \
    && apk add --virtual packgtodel gcc \
    && adduser -S -G www-data -h /var/www/ www-data

ENV LIBRARY_PATH=/lib:/usr/lib

ADD app/requirements.txt /var/www/

RUN pip3 --no-cache-dir install -r /var/www/requirements.txt \
    && apk del packgtodel

ADD docker-deps/nginx/nginx.conf /etc/nginx/nginx.conf
ADD docker-deps/nginx/myPodApp.conf /etc/nginx/conf.d/default.conf
ADD docker-deps/supervisord.ini /etc/supervisor.d/supervisord.ini
ADD app /var/www/

WORKDIR /var/www/

ADD docker-deps/startup.sh /opt/startup.sh

RUN chown -R www-data:www-data /var/tmp/ \
    && chmod 755 /opt/startup.sh

# EXPOSE 80 8000

ENTRYPOINT ["/opt/startup.sh"]
