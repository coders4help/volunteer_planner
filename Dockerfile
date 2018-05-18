#FROM python:3.6-alpine3.7
FROM alpine:3.7
ARG vpbasedir=/opt/vp/
ARG DJANGO_SETTINGS_MODULE=volunteer_planner.settings.production
ARG SECRET_KEY=local
ARG DATABASE_ENGINE=django.db.backends.postgresql_psycopg2
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

RUN apk add --no-cache --virtual .build-deps \
	gcc \
	musl-dev \
	postgresql-dev \
	python3-dev \
	&& \
    apk add --no-cache \
        gettext \
	gettext-lang \
	jq \
        postgresql \
	uwsgi \
	uwsgi-python3 \
	&& \
    pip3 install --upgrade --quiet pip setuptools && \
    pip3 install -r requirements/postgres.txt && \
    pip3 install --upgrade --quiet uwsgitop && \
    apk del --purge .build-deps && \
    /bin/rm -rf /var/cache/apk/* /root/.cache

ADD django-entrypoint.sh /
RUN chmod 0755 /django-entrypoint.sh

USER ${user}
ADD --chown=1000:1000 ./ ${vpbasedir}
RUN python3 manage.py compilemessages --no-color && \
    python3 manage.py collectstatic --clear --noinput --verbosity 0

ENTRYPOINT [ "/django-entrypoint.sh" ]
