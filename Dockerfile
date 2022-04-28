# syntax=docker/dockerfile:1
# auxiliary image
FROM python:3.9-alpine3.14 as build
# Installing uwsgi-plugins will install python3 package as dependency.
# Base image already contains python3, so this dependencies will only
# increase image size without any profit - plus there will be two python
# installations, potentially conflicting with each other.
# So we install plugins and copy needed files later, into our real image.
RUN apk update && \
    apk add --no-cache --no-scripts \
      uwsgi-cache \
      uwsgi-http \
      uwsgi-python3

# This starts the real image.
FROM python:3.9-alpine3.14
# Define some build arguments and their defaults.
ARG VP_BASE_DIR=/opt/vp/
ARG DJANGO_SETTINGS_MODULE=volunteer_planner.settings.production
ARG SECRET_KEY=local
ARG DATABASE_ENGINE=django.db.backends.postgresql
ARG DEV=""
ARG DJANGO_STATIC_ROOT=${VP_BASE_DIR}/static
ARG VP_USER=vp

# Define environment variables, used at runtime.
ENV PYTHONUNBUFFERED=1
ENV STATIC_ROOT=${DJANGO_STATIC_ROOT}
ENV DEBUG=${DEV:+True}

# Add user and group (user home will be created automatically)
RUN addgroup -g 1000 ${VP_USER} && \
    adduser -G ${VP_USER} -u 1000 -D -h ${VP_BASE_DIR} ${VP_USER} && \
    # Add some auxiliary directories used during runtime.
    mkdir -p /run/vp ${STATIC_ROOT} && \
    # Ensure, working user will be able to write
    chown -R ${VP_USER}:${VP_USER} /run/vp ${STATIC_ROOT}

ADD ./requirements ${VP_BASE_DIR}/requirements

# Install required system software (packages).
RUN apk update \
    && \
    apk add --no-cache \
        # remove this package, once requirements are back to pure pypi, without git+https
        git \
        # django compilemessages requires gettext
        gettext \
        # used for healthckeck
        jq \
        # database client
        postgresql-client \
        # server runtime
        uwsgi \
    && \
    # clean up - no-cache should avoid files being created, but there's useless index left
    /bin/rm -rf /var/cache/apk/*

# Install python libraries.
# Avoid caches (either build layer cache catches it or it's useless anyway).
RUN pip3 --no-input --no-cache-dir --disable-pip-version-check \
      install --upgrade --prefer-binary --compile \
      pip \
      setuptools \
      uwsgitop \
    && \
    pip3 --no-input --no-cache-dir --disable-pip-version-check \
      install --upgrade --prefer-binary --compile \
      -r ${VP_BASE_DIR}/requirements/production.txt

# Copy uwsgi-plugins from first build stage.
# That's all, we're interesed in, python installation is part of our base image.
COPY --from=build /usr/lib/uwsgi /usr/lib/uwsgi

# Add entrypoints.
ADD django-entrypoint.sh celery-entrypoint.sh /
RUN chmod 0755 /django-entrypoint.sh /celery-entrypoint.sh

# chdir to our working directory
WORKDIR ${VP_BASE_DIR}
# Change user to our working user
USER ${VP_USER}

# Ddd project contents, owned by ${VP_USER}
ADD --chown=${VP_USER}:${VP_USER} ./ ${VP_BASE_DIR}
# Prepare installation by compiling translations and collecting static
# resources, for usage by reverse HTTP proxy.
RUN python3 manage.py compilemessages --no-color --traceback --verbosity 0 \
    && \
    echo "Translations compiled" \
    && \
    python3 manage.py collectstatic --clear --no-input --traceback --verbosity 0 \
    && \
    echo "Static files collected"

# This is, where the magic happens, during container start
ENTRYPOINT [ "/django-entrypoint.sh" ]
