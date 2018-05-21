FROM python:2.7-alpine
ARG vpbasedir=/opt/vp/
ENV PYTHONUNBUFFERED=1 user=vp

WORKDIR ${vpbasedir}

RUN addgroup -g 1000 ${user} && \
    adduser -G vp -u 1000 -D -h ${vpbasedir} ${user} && \
    chown ${user}:${user} ${vpbasedir}

ADD ./requirements ${vpbasedir}/requirements

RUN apk add --no-cache \
        musl-dev gcc \
        postgresql postgresql-dev \
        uwsgi uwsgi-python \
        gettext gettext-lang && \
    pip install -r requirements/dev_postgres.txt && \
    apk del --purge gcc musl-dev && \
    /bin/rm -rf /var/cache/apk/* && \
    /bin/rm -rf /root/.cache

ADD ./ ${vpbasedir}
RUN mkdir -p /run/vp ${vpbasedir}/static && \
    chmod 0755 django-entrypoint.sh && \
    chown -R vp:vp . /run/vp && \
    /usr/local/bin/python manage.py compile_pyc --path . && \
    /usr/local/bin/python manage.py compilemessages --no-color && \
    /usr/local/bin/python manage.py collectstatic --clear --noinput --verbosity 0

USER ${user}
ENTRYPOINT [ "./django-entrypoint.sh" ]
