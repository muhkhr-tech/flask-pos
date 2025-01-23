FROM postgres:11
ENV TZ='Asia/Makassar'
RUN localedef -i id_ID -c -f UTF-8 -A /usr/share/locale/locale.alias id_ID.UTF-8
ENV LANG id_ID.utf8
ENV POSTGRES_PASSWORD postgres
ENV POSTGRES_DB flask_pos_db
ENV POSTGRES_USER admin
ENV POSTGRES_PASSWORD admin
COPY init.sql /docker-entrypoint-initdb.d/