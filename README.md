# Openstack VIM Driver

A VIM driver implementation that manages infrastructure with Openstack. Create/delete operations are managed with Heat, by first translating the TOSCA template for the infrastructure into a Heat template.

Currently the only external infrastructure that can be returned by the "find infrastructure" API is Networks.

Please read the following guides to get started with the VIM Driver:

- [Install for Python](./docs/install.md) - install the driver from source or production distribution (for use with python)
- [Run](./docs/run.md) - install and run docker/helm chart versions of the driver
- [Deployment Locations](./docs/deployment_locations.md) - details the properties expected by this driver on a Deployment Location
- [Supported Tosca](./docs/supported_tosca.md) - details on supported infrastructure types
- [APIs](./docs/apis.md) - details additional APIs on this driver not expected by a VIM driver
