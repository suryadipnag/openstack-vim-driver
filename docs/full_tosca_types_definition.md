# Tosca Types

Below is the full definition of the extended TOSCA types included in this driver:

```
tosca_definitions_version: tosca_simple_yaml_1_0

description: Custom types supported out-of-the-box by this driver

node_types:
  tosca_definitions_version: tosca_simple_yaml_1_0
description: Test
node_types:
  ##########################
  ## Custom Openstack Types
  ############################
  ## The following types are Openstack specific
  os.nodes.Root:
    derived_from: tosca.nodes.Root

  ### Neutron
  os.datatypes.neutron.AllocationPool:
    derived_from: tosca.datatypes.Root
    properties:
      start:
        description: start address for the allocation pool
        type: string
        required: true
      end:
        description: end address for the allocation pool
        type: string
        required: true
  os.datatypes.neutron.ExtFixedIps:
    derived_from: tosca.datatypes.Root
    properties:
      ip_address:
        description: external fixed IP address
        type: string
        required: false
      subnet:
        description: subnet of external fixed IP address
        type: string
        required: false
  os.datatypes.neutron.ExtGatewayInfo:
    derived_from: tosca.datatypes.Root
    properties:
      enable_snat:
        description: enables Source NAT on the router gateway
        type: boolean
        required: false
      external_fixed_ips:
        description: external fixed IP addresses for the gateway (Mitaka 6.0.0)
        type: list
        entry_schema:
          type: os.datatypes.neutron.ExtFixedIps
        required: false
      network:
        description: ID or name of the external network for the gateway
        type: string
        required: true
  os.datatypes.neutron.HostRouteInfo:
    derived_from: tosca.datatypes.Root
    properties:
      destination:
        description: the destination for static route
        type: string
        required: true
      nexthop:
        description: the next hop for the destination
        type: string
        required: true
  os.datatypes.neutron.SecurityGroupRule:
    derived_from: tosca.datatypes.Root
    properties:
      direction:
        description: >
          The direction in which the security group rule is applied.
          For a compute instance, an ingress security group rule matches traffic that is incoming (ingress) for that instance.
          An egress rule is applied to traffic leaving the instance. Defaults to "ingress"
        type: string
        required: false
      ethertype:
        description: Ethertype of the traffic. Defauts to "IPv4"
        type: string
        required: false
        constraints:
          - value_values: [IPv4, IPv6]
      port_range_max:
        description: >
          The maximum port number in the range that is matched by the security group rule.
          The port_range_min attribute constrains the port_range_max attribute.
          If the protocol is ICMP, this value must be an ICMP type
        type: integer
        required: false
        constraints:
          - in_range: [0, 65535]
      port_range_min:
        description: >
          The minimum port number in the range that is matched by the security group rule.
          If the protocol is TCP or UDP, this value must be less than or equal to the value of the port_range_max attribute.
          If the protocol is ICMP, this value must be an ICMP type
        type: integer
        required: false
        constraints:
          - in_range: [0, 65535]
      protocol:
        description: the protocol that is matched by the security group rule. Valid values include tcp, udp, and icmp
        type: string
        required: false
      remote_group_id:
        description: >
          The remote group ID to be associated with this security group rule.
          If no value is specified then this rule will use this security group for the remote_group_id.
          The remote mode parameter must be set to "remote_group_id"
        type: string
        required: false
      remote_ip_prefix:
        description: the remote IP prefix (CIDR) to be associated with this security group rule
        type: string
        required: false
      remote_mode:
        description: whether to specify a remote group or a remote IP prefix. Defaults to "remote_ip_prefix"
        type: string
        required: false
        constraints:
          - valid_values: [remote_ip_prefix, remote_group_id]

  os.nodes.neutron.Root:
    derived_from: os.nodes.Root
    attributes:
      show:
        description: detailed information about this resource
        type: string

  os.nodes.neutron.Net:
    description: A network is a virtual isolated layer-2 broadcast domain which is typically reserved to the tenant who created it, unless the network has been explicitly configured to be shared
    derived_from: os.nodes.neutron.Root
    properties:
      admin_state_up:
        description: the administrative state of the network
        type: boolean
        required: false
      dhcp_agent_ids:
        description: the IDs of the DHCP agent to schedule the network
        type: list
        entry_schema:
          type: string
        required: false
      dns_domain:
        description: DNS domain associated with this network (Neutron 7.0.0)
        type: string
        required: false
      name:
        description: name of the network
        type: string
        required: false
      port_security_enabled:
        description:  flag to enable/disable port security on the network. It provides the default value for the attribute of the ports created on this network (Libery 5.0.0)
        type: boolean
        required: false
      qos_policy:
        description: the name or ID of QoS policy to attach to this network (Mitaka 6.0.0)
        type: string
        required: false
      shared:
        description: whether this network should be shared across all tenants
        type: boolean
        required: false
        #default: false
      tags:
        description: the tags to be added to the network (Pike 9.0.0+)
        type: list
        entry_schema:
          type: string
        required: false
      tenant_id:
        description: the ID of the tenant which will own the network
        type: string
        required: false
      value_specs:
        description: extra parameters to include (specific to hardware or extensions)
        type: map
        required: false
    attributes:
      admin_state_up:
        description: the administrative status of the network
        type: boolean
      l2_adjacency:
        description: true means that you can expect L2 connectivity throughout the network (Pike 9.0.0)
        type: boolean
      mtu:
        description: the maximum transmission unit size (in bytes) for the network
        type: integer
      name:
        description: the name of the network
        type: string
      port_security_enabled:
        description: true if port security is enabled (Libery 5.0.0)
        type: boolean
      qos_policy_id:
        description: the QoS policy ID attached to this network (Mitaka 6.0.0)
        type: string
      segments:
        description: the segments of this network (Rocky 11.0.0)
        type: list
      status:
        description: the status of the network
        type: string
      subnets:
        description: the IDs of subnets of this network
        type: list
        entry_schema:
          type: string
      tenant_id:
        description: the tenant owning this resource
        type: string
    capabilities:
      link:
        type: tosca.capabilities.network.Linkable

  os.nodes.neutron.Subnet:
    description: A subnet represents an IP address block that can be used for assigning IP addresses to virtual instances. Each subnet must have a CIDR and must be associated with a network. IPs can be either selected from the whole subnet CIDR, or from “allocation pools” that can be specified by the user. (OS::Neutron::Subnet)
    derived_from: os.nodes.neutron.Root
    properties:
      allocation_pools:
        description: start and end addresses for the allocation pools
        type: list
        entry_schema:
          type: os.datatypes.neutron.AllocationPool
        required: false
      cidr:
        description: the CIDR
        type: string
        required: false
      dns_nameservers:
        description: set of DNS name servers to be used
        type: list
        entry_schema:
          type: string
        required: false
        #default: []
      enable_dhcp:
        description: set to true if DHCP is enabled
        type: boolean
        required: false
        #default: true
      gateway_ip:
        description: the gateway IP address
        type: string
        required: false
      host_routes:
        description: a list of host route dictionaries for the subnet
        type: list
        entry_schema:
          type: os.datatypes.neutron.HostRouteInfo
        required: false
      ip_version:
        description: the IP version (4 or 6)
        type: integer
        required: false
        #default: 4
        constraints:
          - valid_values: [4, 6]
      ipv6_address_mode:
        description: IPv6 address mode (Kilo 2015.1)
        type: string
        required: false
        constraints:
          - valid_values: ["dhcpv6-stateful", "dhcpv6-stateless", "slaac"]
      ipv6_ra_mode:
        description: IPv6 router advertisement mode (Kilo 2015.1)
        type: string
        required: false
        constraints:
          - valid_values: ["dhcpv6-stateful", "dhcpv6-stateless", "slaac"]
      name:
        descriptoin: name of the subnet
        type: string
        required: false
      prefixlen:
        description: prefix length for subnet allocation from subnet pool
        type: integer
        required: false
        constraints:
          - greater_or_equal: 0
      segment:
        description: the name/ID of the segment to associate (Rocky 11.0.0) (Pike 9.0.0)
        type: string
        required: false
      subnetpool:
        description: the name/ID of the subnet pool
        type: string
        required: false
      tags:
        description: the tags to be added to the subnet (Pike 9.0.0+)
        type: list
        entry_schema:
          type: string
        required: false
      tenant_id:
        description: the ID of the tenant which will own the subnet
        type: string
        required: false
      value_specs:
        description: extra parameters to include (specific to hardware or extensions)
        type: map
        required: false
        #default: {}
    attributes:
      allocation_pools:
        description: start and end addresses for the allocation pools
        type: list
        entry_schema:
          type: os.datatypes.neutron.AllocationPool
      cidr:
        description: CIDR block notation for this subnet
        type: string
      dns_nameservers:
        description: list of dns dns nameservers
        type: list
        entry_schema:
          type: string
      enable_dhcp:
        description: true if DHCP is enabled for this subnet
        type: boolean
      gateway_ip:
        description: IP of the subnet gateway
        type: string
      host_routes:
        description: additional routes for this subnet
        type: list
        entry_schema:
          type: os.datatypes.neutron.HostRouteInfo
      ip_version:
        description: IP version for this subnet
        type: string
      name:
        description: name of the subnet
        type: string
      network_id:
        description: ID of the parent network
        type: string
      tenant_id:
        description: the tenant owning this resource
        type: string
    requirements:
      - network:
          capability: tosca.capabilities.network.Linkable
          relationship: tosca.relationships.network.LinksTo

  os.nodes.neutron.Router:
    description: Router is a physical or virtual network device that passes network traffic between different networks (OS::Neutron::Router)
    derived_from: os.nodes.neutron.Root
    properties:
      admin_state_up:
        description: the administrative state of the router
        type: boolean
        required: false
        #default: true
      distributed:
        description: indicates whether or not to create a distributed router (Kilo 2015.1)
        type: boolean
        required: false
      external_gateway_info:
        description: external network gateway configuration for a router
        type:  os.datatypes.neutron.ExtGatewayInfo
        required: false
      ha:
        description: indicates whether or not to create a highly available router (Kilo 2015.1)
        type: boolean
        required: false
      l3_agent_ids:
        description: ID list of the L3 agent. User can specify multi-agents for highly available router (Kilo 2015.1)
        type: list
        entry_schema:
          type: string
        required: false
      name:
        description: name of the router
        type: string
        required: false
      tags:
        description: the tags to be added to the router (Pike 9.0.0+)
        type: list
        entry_schema:
          type: string
        required: false
      value_specs:
        description: extra parameters to include (specific to hardware or extensions)
        type: map
        required: false
    attributes:
      admin_state_up:
        description: administrative state of the router
        type: boolean
      external_gateway_info:
        description: gateway network for the router
        type: os.datatypes.neutron.ExtGatewayInfo
      name:
        description: name of the router
        type: string
      status:
        description: status of the router
        type: string
      tenant_id:
        description: the tenant owning this resource
        type: string
  os.nodes.neutron.RouterInterface:
    description: Router interfaces associate routers with existing subnets or ports
    derived_from: os.nodes.neutron.Root
    properties:
      port:
        description: the port, either subnet or port should be specified (Kilo 2015.1)
        type: string
        required: false
      subnet:
        description: the subnet, either subnet or port should be specified
        type: string
        required: false
  os.nodes.neutron.SecurityGroup:
    description: >
      Security groups are sets of IP filter rules that are applied to an instance’s networking.
      They are project specific, and project members can edit the default rules for their group and add new rules sets.
      All projects have a “default” security group, which is applied to instances that have no other security group defined (Icehouse 2014.1)
    derived_from: os.nodes.neutron.Root
    properties:
      description:
        description: description of the security group
        type: string
        required: false
      name:
        description: a string specifying a symbolic name for the security group
        type: string
        required: false
      rules:
        description: list of security group rules
        type: list
        entry_schema:
          type: os.datatypes.neutron.SecurityGroupRule
        required: false
  os.nodes.neutron.SecurityGroupRule:
    description: rules to use in security group resource (Newton 7.0.0)
    derived_from: os.nodes.neutron.Root
    properties:
      direction:
        description: >
          The direction in which the security group rule is applied.
          For a compute instance, an ingress security group rule matches traffic that is incoming (ingress) for that instance.
          An egress rule is applied to traffic leaving the instance. Defaults to "ingress"
        type: string
        required: false
      ethertype:
        description: Ethertype of the traffic. Defauts to "IPv4"
        type: string
        required: false
        constraints:
          - value_values: [IPv4, IPv6]
      port_range_max:
        description: >
          The maximum port number in the range that is matched by the security group rule.
          The port_range_min attribute constrains the port_range_max attribute.
          If the protocol is ICMP, this value must be an ICMP type
        type: integer
        required: false
        constraints:
          - in_range: [0, 65535]
      port_range_min:
        description: >
          The minimum port number in the range that is matched by the security group rule.
          If the protocol is TCP or UDP, this value must be less than or equal to the value of the port_range_max attribute.
          If the protocol is ICMP, this value must be an ICMP type
        type: integer
        required: false
        constraints:
          - in_range: [0, 65535]
      protocol:
        description: >
          the protocol that is matched by the security group rule.
          Allowed values are ah, dccp, egp, esp, gre, icmp, icmpv6, igmp, ipv6-encap, ipv6-frag, ipv6-icmp, ipv6-nonxt, ipv6-opts, ipv6-route, ospf, pgm, rsvp, sctp, tcp, udp, udplite, vrrp and integer representations [0-255]
          Defaults to "tcp"
        type: string
        required: false
        constraints:
          - valid_values: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, ah, dccp, egp, esp, gre, icmp, icmpv6, igmp, ipv6-encap, ipv6-frag, ipv6-icmp, ipv6-nonxt, ipv6-opts, ipv6-route, ospf, pgm, rsvp, sctp, tcp, udp, udplite, vrrp]
      remote_group:
        description: the remote group name or ID to be associated with this security group rule
        type: string
        required: false
      remote_ip_prefix:
        description: the remote IP prefix (CIDR) to be associated with this security group rule
        type: string
        required: false
      security_group:
        description: security group name or ID to add rule
        type: string
        required: true
  ##########################
  ## Extension Types
  ##########################
  ## These types extend original tosca types to provide extra properties/attributes
  os.ext.nodes.network.FloatingIP:
    description: Extension of FloatingIP
    derived_from: tosca.nodes.network.FloatingIP
    properties:
      floating_network:
        type: string
        required: false
    attributes:
      floating_ip_address:
        type: string
    requirements:
      - floating_network:
          description: indicates which network this IP will be on
          capability: tosca.capabilities.network.Linkable
          relationship: tosca.relationships.network.LinksTo
          occurences: [0, 1]
  os.ext.nodes.network.Port:
    description: Extension of Port to include additonal properties allowed on a Neutron port
    derived_from: tosca.nodes.network.Port
    properties:
      security_groups:
        description: List of security group names or IDs. Cannot be used if neutron ports are associated with this server; assign security groups to the ports instead
        type: list
        required: false
  os.ext.nodes.Compute:
    description: Extension of Compute to include additional properties allowed on a Nova server
    derived_from: tosca.nodes.Compute
    properties:
      admin_pass:
        description: The administrator password for the server
        type: string
        required: false
      availability_zone:
        description: Name of the availability zone for server placement
        type: string
        required: false
      config_drive:
        description: If True, enable config drive on the server
        type: boolean
        required: false
      diskConfig:
        description: Control how the disk is partitioned when the server is created
        type: string
        required: false
      flavor:
        description: The ID or name of the flavor to boot onto (you may instead use capability.host properties, which will find the best match based on desired CPU/Mem)
        type: string
        required: false
      flavor_update_policy:
        description: Policy on how to apply a flavor update; either by requesting a server resize or by replacing the entire server
        type: string
        required: false
      image:
        description: The ID or name of the image to boot with
        type: string
        required: false
      image_update_policy:
        description: Policy on how to apply an image-id update; either by requesting a server rebuild or by replacing the entire server
        type: string
        required: false
      key_name:
        description: Name of keypair to inject into the server
        type: string
        required: false
      metadata:
        description: Arbitrary key/value metadata to store for this server. Both keys and values must be 255 characters or less. Non-string values will be serialized to JSON (and the serialized string must be 255 characters or less)
        type: map
        required: false
      name:
        description: Server name
        type: string
        required: false
      reservation_id:
        description: A UUID for the set of servers being requested
        type: string
        required: false
      scheduler_hints:
        description: Arbitrary key-value pairs specified by the client to help boot a server
        type: map
        required: false
      security_groups:
        description: List of security group names or IDs. Cannot be used if neutron ports are associated with this server; assign security groups to the ports instead
        type: list
        required: false
      software_config_transport:
        description: >
          How the server should receive the metadata required for software configuration.
          POLL_SERVER_CFN will allow calls to the cfn API action DescribeStackResource authenticated with the provided keypair. POLL_SERVER_HEAT will allow calls to the Heat API resource-show using the provided keystone credentials.
          POLL_TEMP_URL will create and populate a Swift TempURL with metadata for polling.
          ZAQAR_MESSAGE will create a dedicated zaqar queue and post the metadata for polling
        type: string
        required: false
      user_data:
        description: User data script to be executed by cloud-init. Changes cause replacement of the resource by default, but can be ignored altogether by setting the `user_data_update_policy` property
        type: string
        required: false
      user_data_format:
        description: >
          How the user_data should be formatted for the server.
          For HEAT_CFNTOOLS, the user_data is bundled as part of the heat-cfntools cloud-init boot configuration data.
          For RAW the user_data is passed to Nova unmodified.
          For SOFTWARE_CONFIG user_data is bundled as part of the software config data, and metadata is derived from any associated SoftwareDeployment resources
        type: string
        required: false
      user_data_update_policy:
        description: Policy on how to apply a user_data update; either by ignoring it or by replacing the entire server
        type: string
        required: false
  os.ext.nodes.network.Network:
    derived_from: tosca.nodes.network.Network
    attributes:
      # The following attributes are duplicates of the property definitions on tosca.nodes.network.Network
      # They have been duplicated as the ToscaParser used by this driver does not automatically make properties available as attributes, as required by the TOSCA profile:
      # http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#_Toc445238240
      ip_version:
        type: integer
      cidr:
        type: string
      start_ip:
        type: string
      end_ip:
        type: string
      gateway_ip:
        type: string
      network_name:
        type: string
      network_id:
        type: string
      segmentation_id:
        type: string
      network_type:
        type: string
      physical_network:
        type: string
      dhcp_enabled:
        type: boolean
      # END duplicates
```
