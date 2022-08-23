# Install to Kubernetes

This section details how to install the Openstack driver into a Kubernetes environment with Helm.

## Prerequisites

To complete the install you will need a Kubernetes cluster. 

You will also need a controller machine (can be one of the Kubernetes cluster nodes) to perform the installation from. This machine must have the Helm CLI tool installed and initialised with access to your cluster. Please note that `Helm v3` is required.

## Installation

### Download

Download the Helm chart from the [releases](https://github.com/IBM/openstack-vim-driver/releases) page to your machine.

```
wget https://github.com/IBM/openstack-vim-driver/releases/download/<version>/os-vim-driver-<version>.tgz
```

### Configure

Check out the configurable values of the chart with Helm:

```
helm inspect values os-vim-driver-<version>.tgz
```

The driver has a dependency on Kafka, which it uses to send response messages back to Brent. Therefore it must be installed with access to the same shared Kafka cluster as Brent. 

kafka host value must be set as follows, in values.yaml file of the helm package, depending on the CP4NA versions:

* For pre CP4NA v2.3, the kafka host must be iaf-system-kafka-bootstrap

* For CP4NA v2.3/v2.3+, the kafka host must be cp4na-o-events-kafka-bootstrap  


By default, the driver will attempt to connect to Kafka with the address `cp4na-o-events-kafka-bootstrap:9092`.

If you need to set a different address (or configure any of the other values of the Helm chart) you may do so by creating a custom values file.

```
touch custom-values.yml
```

In this file add any values you wish to override from the chart. For example, to change the Kafka address, add the following:

```
app:
  config:
    override:
      messaging:
        connection_address: "myhost:myport"
```

The driver runs with SSL enabled by default. The installation will generate a self-signed certificate and key by default, adding them to the Kubernetes secret "ovd-tls". To use a custom certificate and key in your own secret, override the properties under "apps.config.security.ssl.secret".

You will reference the custom-values.yml file when installing the chart with Helm.

### Install

Install the chart using the Helm CLI, adding any custom values file if created.

```
helm install os-vim-driver os-vim-driver-<version>.tgz -f custom-values.yml
```

### Confirm 

You can confirm the driver is working by accessing the Swagger UI included to render the API definitions.

Access the UI at `https://your_host:31681/api/driver/ui` e.g. [`http://localhost:31681/api/driver/ui`](http://localhost:31681/api/driver/ui)
