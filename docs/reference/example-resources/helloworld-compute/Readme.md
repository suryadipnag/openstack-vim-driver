# Hello World Example

This basic Resource example deploys a single Compute VM on Openstack.

# Usage

Ensure you have a suitable image and key setup in Openstack. By default this Resource expects an image called `xenial-server-cloudimg-amd64-disk1` and a key called `helloworld` but these may be changed using the input properties.

Use LMCTL v2.2+ to push this Resource into a target LM environment:

```
lmctl project push my-env
```