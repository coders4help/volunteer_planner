# syntax=docker/dockerfile:1
ARG STAGE
FROM vp_django:${STAGE} as django
FROM nginx:1.21-alpine
ARG VP_BASE_DIR=/opt/vp
RUN mkdir -p /opt/vp/static && \
    apk update && \
    apk add \
        curl \
        && \
    /bin/rm -rf /var/cache/apk/* /root/.cache
COPY --from=django ${VP_BASE_DIR}/static /opt/vp/static
ADD nginx.conf /etc/nginx/conf.d/default.conf
