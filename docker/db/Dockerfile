FROM postgres:9-alpine
ARG DATABASE_NAME=volunteer_planner
ARG DATABASE_USER=vp
ARG DATABASE_PW=volunteer_planner

ENV POSTGRES_SECRETS="${POSTGRES_SECRETS:-/var/lib/postgresql/secrets}"
ENV POSTGRES_DB_FILE="${POSTGRES_SECRETS}/db" \
    POSTGRES_USER_FILE="${POSTGRES_SECRETS}/db_user" \
    POSTGRES_PASSWORD_FILE="${POSTGRES_SECRETS}/db_password"

VOLUME ["/pg_backup"]

RUN chown postgres /pg_backup && \
    mkdir -p "${POSTGRES_SECRETS}" && \
    printf "${DATABASE_NAME}" > ${POSTGRES_DB_FILE} && \
    printf "${DATABASE_USER}" > ${POSTGRES_USER_FILE} && \
    printf "${DATABASE_PW}" > ${POSTGRES_PASSWORD_FILE}
