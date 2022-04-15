FROM alpine:3.14
ARG VP_BASE_DIR=/opt/vp/
ARG DJANGO_SETTINGS_MODULE=volunteer_planner.settings.production
ARG SECRET_KEY=local
ARG DATABASE_ENGINE=django.db.backends.postgresql
ARG DEV=""
ARG DJANGO_STATIC_ROOT=${VP_BASE_DIR}/static
ARG VP_USER=vp

ENV PYTHONUNBUFFERED=1
ENV STATIC_ROOT=${DJANGO_STATIC_ROOT}
ENV DEBUG=${DEV:+True}

WORKDIR ${VP_BASE_DIR}

RUN addgroup -g 1000 ${VP_USER} && \
    adduser -G ${VP_USER} -u 1000 -D -h ${VP_BASE_DIR} ${VP_USER} && \
    chown ${VP_USER}:${VP_USER} ${VP_BASE_DIR} && \
    mkdir -p /run/vp ${STATIC_ROOT} && \
    chown -R vp:vp /run/vp ${VP_BASE_DIR} ${STATIC_ROOT}

ADD ./requirements ${VP_BASE_DIR}/requirements

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
        git \
        postgresql \
        libffi-dev \
        py3-pip \
        uwsgi \
        uwsgi-cache \
        uwsgi-http \
        uwsgi-python3 \
        && \
    pip3 install --upgrade --quiet pip setuptools uwsgitop && \
    pip3 install -r requirements/production.txt ${DEV:+-r requirements/dev.txt} && \
    apk del --purge .build-deps && \
    /bin/rm -rf /var/cache/apk/* /root/.cache

ADD django-entrypoint.sh /
RUN chmod 0755 /django-entrypoint.sh

USER ${VP_USER}
ADD --chown=${VP_USER}:${VP_USER} ./ ${VP_BASE_DIR}
RUN python3 manage.py compilemessages --no-color --traceback --verbosity 0 && \
    echo "Translations compiled" && \
    python3 manage.py collectstatic --clear --no-input --traceback --verbosity 0 && \
    echo "Static files collected"

ENTRYPOINT [ "/django-entrypoint.sh" ]
