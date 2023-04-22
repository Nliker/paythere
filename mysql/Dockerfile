FROM --platform=linux/amd64 mysql:5.7

ENV MYSQL_ROOT_PASSWORD test_mysql

RUN rm /etc/my.cnf

ADD ./config /etc/mysql