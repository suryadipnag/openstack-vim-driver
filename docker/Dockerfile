FROM python:3.7-alpine

ARG PYPI_REPO_IP
ENV PYPI_REPO_IP ${PYPI_REPO_IP:-nexus.accanto.com}
ARG PYPI_REPO_PORT
ENV PYPI_REPO_PORT ${PYPI_REPO_PORT:-8081}
ARG PYPI_REPO_URI
ENV PYPI_REPO_URI ${PYPI_REPO_URI:-http://$PYPI_REPO_IP:$PYPI_REPO_PORT/repository/pypi/simple}
ARG DRIVER_VERSION
ENV DRIVER_VERSION ${DRIVER_VERSION:-0.1.0a10}
ARG DRIVER_PORT
ENV DRIVER_PORT ${DRIVER_PORT:-8292}
ARG NUM_PROCESSES
ENV NUM_PROCESSES ${NUM_PROCESSES:-4}
ARG NUM_THREADS
ENV NUM_THREADS ${NUM_THREADS:-2}
ARG WSGI_CONTAINER
ENV WSGI_CONTAINER ${WSGI_CONTAINER:-uwsgi}

RUN addgroup -S ovd \
 && adduser -S ovd -G ovd \
 && mkdir -p /var/ovd \
 && chown -R ovd:ovd /var/ovd \
 && apk add --no-cache bash \
 # These packages need to be installed so that we can install the Python dependencies.
 # We make this virtual so that we can remove them later
 && apk add --no-cache --virtual .build-deps gcc musl-dev libffi-dev openssl-dev python3-dev make \
 && pip3 install --trusted-host $PYPI_REPO_IP --extra-index-url $PYPI_REPO_URI os-vim-driver==$DRIVER_VERSION \
 && apk del .build-deps gcc musl-dev libffi-dev openssl-dev python3-dev make

USER ovd
WORKDIR /home/ovd

EXPOSE 8292

CMD ["ovd"]