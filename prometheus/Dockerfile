FROM ubuntu/nginx

COPY prometheus.yml prometheus.yml
COPY prometheus prometheus
RUN apt-get update && apt-get install -y \
    net-tools \
    iputils-ping \
    iproute2 \
    curl \
    telnet \
    keepalived \
    vim
CMD ["nohup ./prometheus --config.file=prometheus.yml > info.log 2>&1&"]
