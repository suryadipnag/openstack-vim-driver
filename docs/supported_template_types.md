# Template Types

Currently the VIM driver supports two template types, however one of them is only usable when creating infrastructure:

| Template Type | Create Infrastructure | Find Infrastructure |
| --- | --- | --- |
| TOSCA | Y | Y |
| HEAT | Y | N |

Heat is generally easier to use as Tosca requires translation, so it's behaviour depends on whether the types used can be translated or not. See [Supported Tosca](./supports_tosca.md) for more information.