# Openstack VIM Driver

This driver implements the Stratoss&trade; Lifecycle Manager Brent Infrastructure APIs to allow infrastructure to be managed in Openstack.

The driver has been written in Python3 and can be with the publicly available docker image and helm chart.

# Install

The driver can installed on [Kubernetes](./k8s-install.md) using Helm.

# User Guide

The following sections explain how the VIM Driver works and the restrictions it places on the infrastructure templates used for Resources.

- [Infrastructure Templates](infrastructure-templates.md) - supported templates and types for infrastructure
- [Property Handling](property-handling.md) - details how properties for a Resource are handled as inputs and outputs 
- [Deployment Locations](deployment-locations.md) - details the properties expected by this driver on a valid deployment location
- [Openstack Admin API](os-admin-api.md) - additional API available to check Openstack deployment locations are reachable from the driver