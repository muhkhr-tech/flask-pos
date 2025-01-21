FROM postgres:11
ENV POSTGRES_PASSWORD postgres
ENV POSTGRES_DB flask_pos_db
ENV POSTGRES_USER admin
ENV POSTGRES_PASSWORD admin
COPY init.sql /docker-entrypoint-initdb.d/