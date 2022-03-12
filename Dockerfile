#FROM python:3.6-alpine3.7
FROM alpine:3.14
ARG vpbasedir=/opt/vp/
ARG DJANGO_SETTINGS_MODULE=volunteer_planner.settings.production
ARG SECRET_KEY=local
ARG DATABASE_ENGINE=django.db.backends.postgresql
ARG BETA=""
ARG django_static_root=${vpbasedir}/static

ENV PYTHONUNBUFFERED=1 user=vp
ENV STATIC_ROOT=${django_static_root}

WORKDIR ${vpbasedir}

RUN addgroup -g 1000 ${user} && \
    adduser -G ${user} -u 1000 -D -h ${vpbasedir} ${user} && \
    chown ${user}:${user} ${vpbasedir} && \
    mkdir -p /run/vp ${STATIC_ROOT} && \
    chown -R vp:vp /run/vp ${vpbasedir} ${STATIC_ROOT}

ADD ./requirements ${vpbasedir}/requirements

RUN apk update && \
    apk add --virtual .build-deps \
        gcc \
        jpeg-dev \
        musl-dev \
        postgresql-dev \
        python3-dev \
        zlib-dev \
        && \
    apk add \
        gettext \
        gettext-lang \
        jpeg \
        jq \
        postgresql \
        libffi-dev \
        py3-pip \
        uwsgi \
        uwsgi-cache \
        uwsgi-http \
        uwsgi-python3 \
        && \
    pip3 install --upgrade --quiet pip setuptools uwsgitop && \
    pip3 install -r requirements/postgres.txt ${BETA:+-r requirements/dev.txt} && \
    apk del --purge .build-deps && \
    /bin/rm -rf /var/cache/apk/* /root/.cache

ADD django-entrypoint.sh /
RUN chmod 0755 /django-entrypoint.sh

USER ${user}
ADD --chown=1000:1000 ./ ${vpbasedir}
RUN python3 manage.py compilemessages --use-fuzzy --no-color --traceback --verbosity 0 --ignore /usr/lib/python3.9 && \
    echo "Translations compiled" && \
    python3 manage.py collectstatic --clear --no-input --traceback --verbosity 0 && \
    echo "Static files collected"

ENTRYPOINT [ "/django-entrypoint.sh" ]
