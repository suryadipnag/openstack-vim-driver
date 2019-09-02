# Installing with Python

The following guide details how to install and run the VIM driver from a Python environment.

## Install

Install with pip:

```
pip3 install os-vim-driver
```

## Configuration

To customise the configuration of the vim driver, create a new `ovd_config.yml` in the directory you intend to run the driver from. Add the properties you desire to this file, below shows an example of some of the properties you may choose to set:

```
# Set the port the driver runs on
application:
  port: 8292

# Set the kafka address
messaging:
  connection_address: kafka:9092
```

This file will be found by the driver when it is started.

## Start Development Server

The driver can be started with the simple command:

```
ovd-dev
```

## Start Production Server

To run the application in production you will need a WSGI HTTP Server. We have tested and included instructions for both Gunicorn and uWSGI (2 of the recommended options from [Flask](https://flask.palletsprojects.com/en/1.1.x/deploying/wsgi-standalone/)):

### Gunicon

Install gunicorn with pip:

```
pip3 install gunicorn
```

Run the application, specifying the number of worker processes and the port (as the port in the configuration file will be ignored by gunicorn):

```
gunicorn -w 4 -b 127.0.0.1:8292 "osvimdriver:create_wsgi_app()"
```

### uWSGI

Install uwsgi with pip:

```
pip3 install uwsgi
```

Run the application, specifying the number of worker processes and the port (as the port in the configuration file will be ignored by gunicorn):

```
uwsgi --http 127.0.0.1:8292 --processes 4 --threads 2 --module "osvimdriver:create_wsgi_app()"
```

# Access Swagger UI

The Swagger UI can be found at `http://your_host:8292/api/infrastructure/ui` e.g. `http://localhost:8292/api/infrastructure/ui`
