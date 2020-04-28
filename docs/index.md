# Openstack VIM Driver

This driver implements the [Stratoss&trade; Lifecycle Manager](http://servicelifecyclemanager.com/2.1.0/) Brent Resource Driver APIs to allow infrastructure to be managed in Openstack.

The driver has been written in Python3 and can be installed with the publicly available docker image and helm chart.

# Install

The driver can installed on [Kubernetes](./k8s-install.md) using Helm.

# User Guide

The following sections explain how the driver works and the restrictions it places on the Resource package files and deployment locations.

- [Resources](./user-guide/resources.md) - using Openstack based infrastructure in your Resource
- [Property Handling](./user-guide/property-handling.md) - details how properties for a Resource are handled as inputs and outputs during requests
- [Deployment Locations](./user-guide/deployment-locations.md) - details the properties expected by this driver on a valid deployment location
- [Openstack Admin API](./user-guide/os-admin-api.md) - additional API available to check Openstack deployment locations are reachable from the driver

# Example Resources

Two example Resources have been included to demonstrate creating/deleting infrastructure and finding infrastructure:

- [Helloworld Compute](./reference/example-resources/helloworld-compute/Readme.md) - simple Resource which creates a single compute instance in Openstack (TOSCA and HEAT examples included)
- [Neutron Network](./reference/example-resources/neutron-network/Readme.md) - a Resource which supports being found with a piece of discovery infrastructure. Use this Resource as an external reference in an Assembly to link to an existing network in Openstack