# Openstack Admin API

An additional API is offered by this driver, which is not part of the standard VIM driver API. 

Navigate to `api/os/ui/` on your running VIM driver application to find additional APIs for pinging Openstack deployment locations. This API allows you to test your deployment location properties are correct by sending a request to connect to to that location with the Heat client. 

If it returns successfully then the location is reachable and supports Heat, so it is suitable for usage in create/find requests.
