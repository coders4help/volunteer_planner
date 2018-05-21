FROM nginx:1.13-alpine
ARG vpbasedir=/opt/vp
RUN mkdir -p /opt/vp/static && \
    apk update && \
    apk add \
        curl \
        && \
    /bin/rm -rf /var/cache/apk/* /root/.cache
COPY --from=vp_django:latest ${vpbasedir}/static /opt/vp/static
ADD nginx.conf /etc/nginx/conf.d/default.conf
