# Tosca Types

The following YAML files define the custom TOSCA types provided by this driver:

- [Openstack Type Extensions](tosca-type-definitions/type_extensions.yaml) - extensions on the TOSCA simple profile and types that map one-to-one to HEAT types

The use types from the following files you must add an import to your TOSCA template:

```
imports:
  - etsi_nfv_sol001
```

- [NFV Sol001 Common Types](tosca-type-definitions/etsi_nfv_sol001_common_types.yaml) - ETSI NFV SOL 001 common types definitions version 2.6.1
- [NFV Sol001 VNFD Types](tosca-type-definitions/etsi_nfv_sol001_vnfd_types.yaml) - ETSI NFV SOL 001 vnfd types definitions version 2.6.1
- [NFV Extensions](tosca-type-definitions/nfv_extensions) - extensions provided to add Openstack specifics to ETSI NFV types
