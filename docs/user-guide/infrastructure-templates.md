# Infrastructure Templates

Infrastructure Templates are text files which describe infrastructure and can be of any type supported by this driver. Currently the Openstack VIM driver supports two template types, however one of them is only usable when creating infrastructure:

| Template Type | Create Infrastructure | Find Infrastructure |
| --- | --- | --- |
| TOSCA | Y | Y |
| HEAT | Y | N |

Heat is generally easier to use as Tosca requires translation, so it's behaviour depends on whether the types used can be translated or not. The API for create and find infrastructure requests specifies that templates are passed to the driver to describe the infrastructure.

# Heat Support

The Openstack VIM driver uses the Heat API to create infrastructure, which means any template supported by the version of Heat on your Openstack environment will work fine.

We recommend reading through the Openstack [Template Guide](https://docs.openstack.org/heat/train/template_guide/) to learn about the Heat template syntax.

# TOSCA Support

The Openstack VIM driver can create any TOSCA types, from v1.0 of the [simple profile](http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html), that are translatable to a known Heat type. The ability to translate is determined by two aspects:

- the conversion support offered in the [heat translator](https://github.com/accanto-systems/heat-translator/tree/accanto) library used by this driver
- additional types provided by this driver

The following sections detail how particular types are implemented by this driver and details any limitations to using them.

# Compute

| API    | Supported |
| ------ | --------- |
| Create | Y         |
| Find   | N         |

Using the `tosca.nodes.Compute` or `os.ext.nodes.Compute` type will result in an `OS::Nova::Server` being created in the target Openstack environment.

## Create

### Properties and Attributes

The TOSCA specification for `tosca.nodes.Compute` declares no properties. However, a custom extension named `os.ext.nodes.Compute` is automatically added to all templates, which enables additional properties supported by Heat:

- admin_pass
- availability_zone
- config_drive
- diskConfig
- flavor
- flavor_update_policy
- image
- image_update_policy
- key_name
- metadata
- name
- reservation_id
- scheduler_hints
- security_groups
- software_config_transport
- user_data
- user_data_format
- user_data_update_policy

The complete definition of `os.ext.nodes.Compute` can found at [Full Types Definition](../reference/full_tosca_types_definition.md)

The TOSCA specification for `tosca.nodes.Compute` declares 4 attributes, however only `private_address` can currently be used with this driver. This will return the IP address of the server on the private network.

Although the TOSCA specification states all properties should be available as attributes, the translator being used by this driver currently does not support this.

### Host Capability

The properties of the `host` capability on a `tosca.nodes.Compute` are used to calculate the `image` and `flavor` to be used by the `OS::Nova::Server`, unless properties of the same name are set on the node instead (the extension type `os.ext.nodes.Compute` defines these additional properties, leave them empty to allow calculation to take place).

Currently, the translator used by this driver only supports a pre-defined list of flavors and images:

Flavor:

```
'm1.xlarge': {'mem_size': 16384, 'disk_size': 160, 'num_cpus': 8},
'm1.large': {'mem_size': 8192, 'disk_size': 80, 'num_cpus': 4},
'm1.medium': {'mem_size': 4096, 'disk_size': 40, 'num_cpus': 2},
'm1.small': {'mem_size': 2048, 'disk_size': 20, 'num_cpus': 1},
'm1.tiny': {'mem_size': 512, 'disk_size': 1, 'num_cpus': 1},
'm1.micro': {'mem_size': 128, 'disk_size': 0, 'num_cpus': 1},
'm1.nano': {'mem_size': 64, 'disk_size': 0, 'num_cpus': 1}
```

Images:

```
'ubuntu-software-config-os-init': {'architecture': 'x86_64', 'os_type': 'linux', 'os_distro': 'ubuntu', 'os_version': '14.04' },
'ubuntu-12.04-software-config-os-init': {'architecture': 'x86_64', 'os_type': 'linux', 'os_distro': 'ubuntu', 'os_version': '12.04' },
'fedora-amd64-heat-config': {'architecture': 'x86_64', 'os_type': 'linux', 'os_distro': 'fedora', 'os_version': '18.0' },
'F18-x86_64-cfntools': {'architecture': 'x86_64', 'os_type': 'linux', 'os_distro': 'fedora', 'os_version': '19' },
'Fedora-x86_64-20-20131211.1-sda': {'architecture': 'x86_64', 'os_type': 'linux', 'os_distro': 'fedora', 'os_version': '20' },
'cirros-0.3.1-x86_64-uec': {'architecture': 'x86_64', 'os_type': 'linux', 'os_distro': 'cirros', 'os_version': '0.3.1' },
'cirros-0.3.2-x86_64-uec': {'architecture': 'x86_64', 'os_type': 'linux', 'os_distro': 'cirros', 'os_version': '0.3.2' },
'rhel-6.5-test-image': {'architecture': 'x86_64', 'os_type': 'linux', 'os_distro': 'rhel', 'os_version': '6.5'}
```

# Network

| API    | Supported |
| ------ | --------- |
| Create | Y         |
| Find   | Y         |

Using the `tosca.nodes.network.Network` type will result in a `OS::Neutron::Network` and `OS::Neutron::Subnet` being created in the target Openstack environment. It also possible, when creating infrastructure, to reference existing networks instead of creating them.

## Create

### Properties and Attributes

The following table details the supported properties when creating a network using the `tosca.nodes.network.Network` specification:

| Tosca Property   | Supported | Details                                                                                                          |
| ---------------- | --------- | ---------------------------------------------------------------------------------------------------------------- |
| ip_version       | Y         | Set on the subnet                                                                                                |
| cidr             | Y         | Set on the subnet                                                                                                |
| start_ip         | Y         | Sets the `start` property on the single allocation pool added to the subnet                                      |
| end_up           | Y         | Sets the `end` property on the single allocation pool added to the subnet                                        |
| network_name     | Y         | Set on the network. Also used as the subnet name by prefixing with `_subnet`                                     |
| network_id       | N         | Should not be set when creating a network, only to find an existing one                                          |
| segmentation_id  | Y         | Sets the `provider:segmentation_id` property on the network                                                      |
| network_type     | N         | Hardcoded to `vxlan` by the translator as this do not appear on the current `OS::Neutron::Network` specification |
| physical_network | N         | -                                                                                                                |
| dhcp_enabled     | Y         | Sets the `enable_dhcp` property on the subnet                                                                    |

Although the TOSCA specification states all properties should be available as attributes, the translator being used by this driver currently does not support this. This means it is not possible to use the `get_attribute` function to make use of their values elsewhere in the template.

### Reference existing network on create

When creating infrastructure, the TOSCA template may reference an existing network by adding a node of type `tosca.nodes.network.Network`. To indicate the network should be found, instead of created, either:

- Set `network_name` and do NOT set `cidr`
- Set `network_id`

## Find

When finding an existing/external network using the find infrastructure API, the rules are different to a Create. The driver will use the Neutron API directly to retrieve information about the network and subnet. As a result, more attributes are available. A custom extension named `os.ext.nodes.network.Network` is automatically added to all templates, which enables additional attributes to be retrieved as outputs from the template:

- ip_version
- cidr
- start_ip
- end_ip
- gateway_ip
- network_name
- network_id
- segmentation_id
- network_type
- physical_network
- dhcp_enabled

The complete definition of `os.ext.nodes.network.Network` can found at [Full Types Definition](../reference/full_tosca_types_definition.md).

This project also includes a reference implementation of a Resource to be used as an "external reference" in LM, which makes use of the find infrastructure API to discover an existing network and return it's attributes. It can be found at `example-resources/neutron-network`.

# Floating IP

An extension type named `os.ext.nodes.network.FloatingIP` has been included which supports setting the `floating_network` through a requirement instead of a property.

It also supports the `floating_ip_address` attribute.

# Port

An extension type named `os.ext.nodes.network.Port` has been included which supports a `security_groups` property so that a port may be associated to security groups.

# Other Heat Types

This VIM driver also includes additional types which map almost one-to-one with their equivalent Heat type.

The following types have been added:

| Tosca Type                         | Heat Type Equivalent           |
| ---------------------------------- | ------------------------------ |
| os.nodes.neutron.Net               | OS::Neutron::Net               |
| os.nodes.neutron.Subnet            | OS::Neutron::Subnet            |
| os.nodes.neutron.Router            | OS::Neutron::Router            |
| os.nodes.neutron.RouterInterface   | OS::Neutron::RouterInterface   |
| os.nodes.neutron.SecurityGroup     | OS::Neutron::SecurityGroup     |
| os.nodes.neutron.SecurityGroupRule | OS::Neutron::SecurityGroupRule |

The complete definition of these TOSCA types can be found at [Full Types Definition](../reference/full_tosca_types_definition.md).
