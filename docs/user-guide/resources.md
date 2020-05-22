# Resources

The Openstack driver allows you to create Stacks in a target Openstack as part of a `Create` lifecycle transition (then remove the Stack with `Delete`). This is done by configuring the use of the driver on Create/Delete and by including Heat or Tosca templates in your Resource package. 

The driver also supports finding existing Networks in a target Openstack when attempting to find an external reference Resource (in an Assembly design).

# Resource Descriptor

Openstack driver should only be used on Create/Delete transitions.

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

Attempts to use the driver on other transitions will result in an error.

**Note:** it's rare you need to do this but if you do not onboard the Openstack driver with type `openstack` then this value must be renamed to your chosen type.

You may also use the driver when finding an external reference:

```
queries:
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

Infrastructure Templates are text files which describe infrastructure and can be of any type supported by this driver. Currently the Openstack VIM driver supports two template types, however only one of them may be used to find references to externally managed infrastructure:

| Template Type | Execute Lifecycle (Create Infrastructure) | Find References |
| --- | --- | --- |
| TOSCA | Y | Y |
| HEAT | Y | N |

Heat is generally easier to use as Tosca requires translation, so it's behaviour depends on whether the types used can be translated or not.

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

To use TOSCA when finding references to your externally managed Resource, add a template to your Resource package with the name `discover.yaml` or `discover.yml`:

```
Lifecycle/
  openstack/
    discover.yaml
```

To read more about the TOSCA types supported by this driver, see [TOSCA templates](./tosca-templates.md)
