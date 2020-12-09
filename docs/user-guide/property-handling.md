# Property Handling

This section describes how properties are used as inputs and returned as outputs for create and find infrastructure requests. It is important to understand how this works so you may build configurable infrastructure templates which make use of properties passed down by the Stratoss&;trade Lifecycle Manager (LM).

# Execute Lifecycle Requests

On an execute lifecycle (Create) request, the driver will be passed the values for this instance of the Resource for any properties specified on its descriptor.

The Openstack VIM driver allows any of these values to be referenced in a TOSCA or HEAT by passing them as inputs (parameters for HEAT). The value of any property will be set as the value of any input with the same name. 

For example, taking this descriptor:

```
properties:
  prop_a:
    type: string
  prop_b: 
    type: string
  prop_c: 
    type: string
```

Any of the above properties may be used as inputs, with the same name, on a template (i.e. value of prop_a from above will be passed to prop_a on the template, same for prop_b).

**TOSCA:**

```
topology_template:
  inputs:
    prop_a:
      type: string
    prop_b:
      type: string
```

**HEAT:**

```
parameters:
  prop_a:
    type: string
  prop_b:
    type: string
```

Heat supports the following parameter types (correct for Rocky-Victoria releases): string, number, boolean, json (JSON formatted map/list), comma separated list. As TNCO (ALM) supports it's own set of property types it's important that each parameter in your Heat template uses the correct type associated with the type given to the property in the Resource descriptor. For example:

**Descriptor:**

```
properties:
  prop_a:
    type: string
  prop_b:
    type: boolean
  prop_c:
    type: float
```
**HEAT:**

```
parameters:
  prop_a:
    type: string
  prop_b:
    type: boolean
  prop_c:
    type: number
```

You may refer to the table below to select the correct types:

| Resource Descriptor Type | Heat Template Type |
| --- | --- | 
| string | string |
| integer | number |
| float | number |
| boolean | boolean | 
| timestamp | string |
| map | json |
| list | json | 
| custom data type | json |
| key | string (see [keys](#keys)) | 

> Note: as you'll see from the table above; maps, lists and custom data types are converted to JSON strings.

> Note: you'll notice the `comma separated list` Heat type has no matching Resource descriptor type. This type is, in simple terms, a formatted string so if you must use it in your Heat template then set the Resource descriptor type to string (and enter a comma separated list for all values).

## Keys

A Resource descriptor can also include properties of type `key` to reference key pairs created as part of other Resource infrastructure or onboarded manually into Stratoss LM. 

**Descriptor:**
```
properties:
  my_key:
    type: key
```

When a key property is used, the VIM driver has access to 3 components of the key pair: 

- name of the key
- private key
- public key. 

To reference the name of the key, use the property name from the descriptor, as you would for any non-key property. To reference the private key, use the property name and the suffix `_private`. To reference the public key, use the property name and the suffix `_public`:

**TOSCA:**

```
topology_template:
  inputs:
    my_key:
      type: string
    my_key_private:
      type: string
    my_key_public:
      type: string
```

**HEAT:**

```
parameters:
  my_key:
    type: string
  my_key_private:
    type: string
  my_key_public:
    type: string
```

## System Properties

In addition, the `systemProperties` sent by Brent to the driver may be referenced using the property name prefixed with `system_` (to avoid collision with properties using the same names as a system property). For example: `system_resourceId` can be used to reference ID of the Resource and `system_resourceName` can be used to reference the name of the Resource.


**TOSCA:**

```
topology_template:
  inputs:
    system_resourceId:
      type: string
    system_resourceName:
      type: string
```

**HEAT:**

```
parameters:
  system_resourceId:
    type: string
  system_resourceName:
    type: string
```

# Execute Lifecycle Outputs

All outputs from the TOSCA or HEAT template will be passed back by the Openstack VIM driver after creating the infrastructure. Brent will handle matching the outputs with any properties of the same name in a descriptor. 

For example, taking this descriptor:

```
properties:
  prop_a:
    type: string
```

With the following templates, all of the outputs will be returned and are usable in any later lifecycle transitions. However, Brent will match the value of output `prop_a` with the property from the descriptor with the same name, so it will return this value up to LM (making it's value visible in the LM UI).

**TOSCA:**

```
topology_template:
  outputs:
    prop_a:
      value: { get_attribute: [node, some_prop_a] }
    prop_b
      value: { get_attribute: [node, some_prop_b] }
```

**HEAT:**

```
outputs:
  prop_a:
    value: { get_attr: [node, some_prop_a] }
  prop_b:
    value: { get_attr: [node, some_prop_b] }
```

# Find Reference Requests

On a find request, there is only a single input property sent to the driver: instance name. This value is passed by the Openstack VIM driver to the template as an input called `instance_name`.

**Note:** remember only TOSCA templates are currently supported for finding infrastructure

**TOSCA:**

```
topology_template:
  inputs:
    instance_name:
      type: string
```


# Find Reference Outputs

Similar to a create request, all outputs from the TOSCA template will be passed back by the Openstack VIM driver if infrastructure is found. Brent will handle matching the outputs with any properties of the same name in a descriptor. 
