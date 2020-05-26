# TOSCA NFV Types

The following sections detail how particular types from the NFV profile may be used in a TOSCA template deployed by this driver.

Full TOSCA type definitions can be found in [references](reference/full_tosca_types_definition.md)

To use these types you must add a special import to your TOSCA template:

```
imports:
  - etsi_nfv_sol001
```

# tosca.nodes.nfv.Vdu.Compute

Using this type will result in an `OS::Nova::Server` being created in the target Openstack environment.

If set, the `virtual_compute` capability will result in a new `OS::Nova::Flavor` being created for the server. You may use the `flavor` property below to override this behaviour.

An extension type has been provided, named `tosca.nodes.nfv.Vdu.Compute.NovaServer`, which allows you to add the following Openstack specific properties: 

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
- user_data_params
- user_data_format
- user_data_update_policy

Use `user_data_params` if to provided parameters to be templated into `user_data`. E.g. the generated heat will be:

```yaml
user_data:
    str_replace:
        params: 
            <user_data_params>
        template: 
            <user_data>
```

# tosca.nodes.nfv.VduCp

Using this type will result in an `OS::Neutron::Port` being created in the target Openstack environment.

The `order` property may be used to order properties on a target server. 

The `vnic_type` property may be used to the `binding:vnic_type` of the port.

The `virtual_binding` requirement should reference the name of a `Vdu.Compute` node in the template. 

The `virtual_link` requirement should reference the name of a `VnfVirtualLink` node in the template. 

An extension type has been provided, named `tosca.nodes.nfv.VduCp.NeutronPort`, which allows you to add the following Openstack specific properties: 

- name
- admin_state_up
- allowed_address_pairs
- binding_vnic_type
- device_id
- device_owner
- dns_name
- fixed_ips
- mac_address
- port_security_enabled
- qos_policy
- security_groups
- tags
- value_specs

# tosca.nodes.nfv.VnfVirtualLink

Also see the [alternative VnfVirtualLink type](#tosca.nodes.nfv.VnfVirtualLink.NeutronNetwork)

Using this type will result in an `OS::Neutron::Network`, and possibly a `OS::Neutron::Subnet`,  `OS::Neutron::QoSBandwidthLimitRule` and `OS::Neutron::QoSPolicy`, being created in the target Openstack environment.

The following TOSCA results in the following Heat:

TOSCA
```yaml
node_templates:
    VL1:
      type: tosca.nodes.nfv.VnfVirtualLink
      properties:
        connectivity_type:
          layer_protocols: [ ipv4 ]
        description: Internal Virtual link in the VNF
        vl_profile:
          max_bitrate_requirements:
            root: 1048576
            leaf: 1048576
          min_bitrate_requirements:
            root: 1048576
            leaf: 1048576
          virtual_link_protocol_data:
            - associated_layer_protocol: ipv4
              l3_protocol_data:
                ip_version: ipv4
                cidr: 11.11.0.0/24
```

HEAT
```yaml
resources:
  VL1:
    type: OS::Neutron::Net
    properties:
      qos_policy: { get_resource: VL1_qospolicy }
  VL1_subnet:
    type: OS::Neutron::Subnet
    properties:
      network: { get_resource: VL1 }
      ip_version: 4
      cidr: 11.11.0.0/24
  VL1_bandwidth:
    type: OS::Neutron::QoSBandwidthLimitRule
    properties:
      max_kbps: 1024
      policy: { get_resource: VL1_qospolicy }
  VL1_qospolicy:
    type: OS::Neutron::QoSPolicy
```

# tosca.nodes.nfv.VnfVirtualLink.NeutronNetwork

This type is NOT an extension of `tosca.nodes.nfv.VnfVirtualLink`, instead it is an alternative which is useful when you need to reference an existing network by name.

To reference an existing network by name, you only need to provide the Network property:

```yaml
topology_template:
  node_templates:
    mgmt_network_node:
      type: tosca.nodes.nfv.VnfVirtualLink.NeutronNetwork
      properties:
      name: { get_input: mgmt_network }
```

This is useful when you want to create a port on an existing network:

```yaml
topology_template:
  node_templates:
    mgmt_network:
      type: tosca.nodes.nfv.VnfVirtualLink.NeutronNetwork
      properties:
        name: mgmt

    mgmt_port:
      type: tosca.nodes.nfv.VduCp.NeutronPort
      properties:
        name: 'mgmt_port'
      requirements:
        - virtual_binding: compute_node
        - virtual_link: mgmt_network

    compute_node:
      type: tosca.nodes.nfv.Vdu.Compute.NovaServer
      properties:
        name: compute-server
        ...remaining properties...      
```

Results in the following Heat:

```yaml
resources:
  mgmt_port:
    type: OS::Neutron::Port
    properties:
      network: mgmt
  compute_node:
    type: OS::Nova::Server
    properties:
      name: compute-server
      ...remaining properties...      
```