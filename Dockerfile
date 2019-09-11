FROM python:3.6

WORKDIR /etc

COPY install.sh /etc
COPY lib /etc/lib

RUN ./install.sh
