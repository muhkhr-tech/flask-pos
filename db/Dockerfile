FROM mysql:8
ENV MYSQL_ROOT_PASSWORD=root
ENV MYSQL_DATABASE=flask_pos_db
ENV MYSQL_USER=admin
ENV MYSQL_PASSWORD=admin
COPY ./init.sql /docker-entrypoint-initdb.d