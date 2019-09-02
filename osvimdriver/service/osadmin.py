import osvimdriver.api_specs as api_specs
import os
import logging
import pathlib
from ignition.service.framework import Capability, Service, interface, ServiceRegistration
from ignition.service.api import BaseController
from ignition.boot.connexionutils import build_resolver_to_instance
from ignition.service.config import ConfigurationPropertiesGroup
from osvimdriver.openstack.environment import OpenstackDeploymentLocationTranslator

logger = logging.getLogger(__name__)

# Grabs the __init__.py from the api_specs package then takes it's parent, the api directory itself
api_spec_path = str(pathlib.Path(api_specs.__file__).parent.resolve())


class OpenstackAdminProperties(ConfigurationPropertiesGroup):

    def __init__(self):
        super().__init__('openstack_admin')
        self.enabled = True


class OpenstackAdminApiConfigurator():

    def __init__(self):
        pass

    def configure(self, configuration, service_register, service_instances, api_register):
        self.__configure_api_spec(configuration, service_register, service_instances, api_register)

    def __configure_api_spec(self, configuration, service_register, service_instances, api_register):
        admin_properties = configuration.property_groups.get_property_group(OpenstackAdminProperties)
        if admin_properties.enabled is True:
            logger.debug('Configuring Openstack Admin API')
            api_spec = os.path.join(api_spec_path, 'openstack_admin.yaml')
            api_service_class = service_register.get_service_offering_capability(OpenstackAdminApiCapability)
            if api_service_class is None:
                raise ValueError('No service has been registered with the OpenstackAdminApiCapability')
            api_service_instance = service_instances.get_instance(api_service_class)
            if api_service_instance is None:
                raise ValueError('No instance of the OpenstackAdminApiCapability service has been built')
            api_register.register_api(api_spec, resolver=build_resolver_to_instance(api_service_instance))
        else:
            logger.debug('Disabled: Openstack Admin API')


class OpenstackAdminServiceConfigurator():

    def __init__(self):
        pass

    def configure(self, configuration, service_register):
        admin_properties = configuration.property_groups.get_property_group(OpenstackAdminProperties)
        if admin_properties.enabled is True:
            logger.debug('Configuring Openstack Admin Services')
            service_register.add_service(ServiceRegistration(OpenstackAdminApiService, service=OpenstackAdminCapability))
            service_register.add_service(ServiceRegistration(OpenstackAdminService, OpenstackDeploymentLocationTranslator()))
        else:
            logger.debug('Disabled: Openstack Admin Services')


class OpenstackAdminApiCapability(Capability):

    @interface
    def ping(self, **kwarg):
        pass


class OpenstackAdminCapability(Capability):

    @interface
    def ping(self, deployment_location):
        pass


class OpenstackAdminApiService(Service, OpenstackAdminApiCapability, BaseController):

    def __init__(self, **kwargs):
        if 'service' not in kwargs:
            raise ValueError('No service instance provided')
        self.service = kwargs.get('service')

    def ping(self, **kwarg):
        body = self.get_body(kwarg)
        deployment_location = self.get_body_required_field(body, 'deploymentLocation')
        ping_response = self.service.ping(deployment_location)
        response = {'success': ping_response.success, 'description': ping_response.description}
        return (response, 200)


class OpenstackAdminService(Service, OpenstackAdminCapability):

    def __init__(self, location_translator):
        self.location_translator = location_translator

    def ping(self, deployment_location):
        openstack_location = self.location_translator.from_deployment_location(deployment_location)
        heat_driver = openstack_location.heat_driver
        try:
            list_of_stacks = heat_driver.get_stacks()
            for stack in list_of_stacks:
                # Yield first response to force connection
                break
            return PingResponse(True, 'Reached Heat client successfully')
        except Exception as e:
            return PingResponse(False, str(e))


class PingResponse:

    def __init__(self, success, description):
        self.success = success
        self.description = description
