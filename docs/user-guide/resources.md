# Resources

The Openstack driver may only be used for `Create` and `Delete` lifecycle transitions.

Example descriptor:
```
lifecycle:
  Create:
    drivers:
      openstack:
        selector:
          infrastructure-type:
            Openstack
  Delete:
    drivers:
      openstack:
        selector:
          infrastructure-type:
            Openstack
```
# Resource Packages

A Resource using Openstack infrastructure must include either TOSCA or Heat templates in the `Lifecycle` directory of the package:

```
Lifecycle/
  openstack/
    heat.yaml
    tosca.yaml
    discover.yaml
```

**Note:** it's rare you need to do this but if you do not onboard the Openstack driver with type `openstack` then the directory above must be renamed to your chosen type. 

Infrastructure Templates are text files which describe infrastructure and can be of any type supported by this driver. Currently the Openstack VIM driver supports two template types, however one of them is only usable when creating infrastructure:

| Template Type | Execute Lifecycle (Create Infrastructure) | Find References |
| --- | --- | --- |
| TOSCA | Y | Y |
| HEAT | Y | N |

Heat is generally easier to use as Tosca requires translation, so it's behaviour depends on whether the types used can be translated or not. The API for create and find infrastructure requests specifies that templates are passed to the driver to describe the infrastructure.

## Heat Support

The Openstack VIM driver uses the Heat API to create infrastructure, which means any template supported by the version of Heat on your Openstack environment will work fine.

We recommend reading through the Openstack [Template Guide](https://docs.openstack.org/heat/train/template_guide/) to learn about the Heat template syntax.

To use Heat, add a template to your Resource package with the name `heat.yaml` or `heat.yml`:

```
Lifecycle/
  openstack/
    heat.yaml
```

## TOSCA Support

The Openstack VIM driver can create any TOSCA types from v1.0 of the [simple profile](http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html) that are translatable to a known Heat type. The ability to translate is determined by two aspects:

- the conversion support offered in the [heat translator](https://github.com/accanto-systems/heat-translator/tree/accanto) library used by this driver
- additional types provided by this driver

To use TOSCA when creating infrastructure, add a template to your Resource package with the name `tosca.yaml` or `tosca.yml`:

```
Lifecycle/
  openstack/
    tosca.yaml
```

To use TOSCA when finding references, add a template to your Resource package with the name `discover.yaml` or `discover.yml`:

```
Lifecycle/
  openstack/
    discover.yaml
```

To read more about the TOSCA types supported by this driver, see [TOSCA templates](./tosca-template.md)