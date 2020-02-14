import uuid
import logging
import re
from ignition.service.framework import Service, Capability, interface
from ignition.service.infrastructure import InfrastructureDriverCapability, InfrastructureNotFoundError, InvalidInfrastructureTemplateError
from ignition.model.infrastructure import CreateInfrastructureResponse, DeleteInfrastructureResponse, FindInfrastructureResponse, FindInfrastructureResult, InfrastructureTask, STATUS_IN_PROGRESS, STATUS_COMPLETE, STATUS_FAILED, STATUS_UNKNOWN
from ignition.model.failure import FailureDetails, FAILURE_CODE_INFRASTRUCTURE_ERROR
from osvimdriver.service.tosca import ToscaValidationError, NotDiscoveredError
from osvimdriver.openstack.heat.driver import StackNotFoundError
from ignition.utils.propvaluemap import PropValueMap

logger = logging.getLogger(__name__)

OS_STACK_STATUS_CREATE_IN_PROGRESS = 'CREATE_IN_PROGRESS'
OS_STACK_STATUS_CREATE_COMPLETE = 'CREATE_COMPLETE'
OS_STACK_STATUS_CREATE_FAILED = 'CREATE_FAILED'
OS_STACK_STATUS_ADOPT_IN_PROGRESS = 'ADOPT_IN_PROGRESS'
OS_STACK_STATUS_ADOPT_COMPLETE = 'ADOPT_COMPLETE'
OS_STACK_STATUS_ADOPT_FAILED = 'ADOPT_FAILED'
OS_STACK_STATUS_DELETE_IN_PROGRESS = 'DELETE_IN_PROGRESS'
OS_STACK_STATUS_DELETE_COMPLETE = 'DELETE_COMPLETE'
OS_STACK_STATUS_DELETE_FAILED = 'DELETE_FAILED'

TOSCA_TEMPLATE_TYPE = 'TOSCA'
HEAT_TEMPLATE_TYPE = 'HEAT'

DELETE_REQUEST_PREFIX = 'Del-'

class StackNameCreator:

    def create(self, resource_id, resource_name):
        potential_name = '{0}.{1}'.format(resource_name, resource_id)
        needs_starting_letter = not potential_name[0].isalpha()
        potential_name = re.sub('[^A-Za-z0-9_.-]+', '', potential_name)
        max_size = 254 if needs_starting_letter else 255
        while len(potential_name)>max_size:
            potential_name = potential_name[1:]
        if needs_starting_letter:
            potential_name = 's{0}'.format(potential_name)
        return potential_name

class PropertiesMerger:

    def merge(self, properties, system_properties):
        new_props = {k:v for k,v in properties.items_with_types()}
        for k, v in system_properties.items_with_types():
            new_key = 'system_{0}'.format(k)
            new_props[new_key] = v
        return PropValueMap(new_props)

class InfrastructureDriver(Service, InfrastructureDriverCapability):

    def __init__(self, location_translator, **kwargs):
        if 'heat_translator_service' not in kwargs:
            raise ValueError('heat_translator_service argument not provided')
        self.heat_translator = kwargs.get('heat_translator_service')
        if 'tosca_discovery_service' not in kwargs:
            raise ValueError('tosca_discovery_service argument not provided')
        self.tosca_discovery_service = kwargs.get('tosca_discovery_service')
        self.location_translator = location_translator
        self.stack_name_creator = StackNameCreator()
        self.props_merger = PropertiesMerger()
 
    def create_infrastructure(self, template, template_type, system_properties, properties, deployment_location):
        openstack_location = self.location_translator.from_deployment_location(deployment_location)
        heat_driver = openstack_location.heat_driver
        if 'stack_id' in properties:
            stack_id = properties.get('stack_id')
            if stack_id != None and len(stack_id.strip())!=0 and stack_id.strip() != "0":
                try:
                    ##Check for valid stack
                    heat_driver.get_stack(stack_id.strip())
                except StackNotFoundError as e:
                    raise InfrastructureNotFoundError(str(e)) from e
                return CreateInfrastructureResponse(stack_id, stack_id)
        if template_type.upper() == TOSCA_TEMPLATE_TYPE.upper():
            try:
                heat_template = self.heat_translator.generate_heat_template(template)
            except ToscaValidationError as e:
                raise InvalidInfrastructureTemplateError(str(e)) from e
            logger.debug('Translated Tosca template:\n%s\nto Heat template:\n%s', template, heat_template)
        elif template_type.upper() == HEAT_TEMPLATE_TYPE.upper():
            heat_template = template
        else:
            raise InvalidInfrastructureTemplateError('Cannot create using template of type \'{0}\'. Must be one of: {1}'.format(template_type, [TOSCA_TEMPLATE_TYPE, HEAT_TEMPLATE_TYPE]))
        heat_input_util = openstack_location.get_heat_input_util()
        input_props = self.props_merger.merge(properties, system_properties)
        heat_inputs = heat_input_util.filter_used_properties(heat_template, input_props)
        if 'resourceId' in system_properties and 'resourceName' in system_properties:
            stack_name = self.stack_name_creator.create(system_properties['resourceId'], system_properties['resourceName'])
        else:
            stack_name = 's' + str(uuid.uuid4())
        stack_id = heat_driver.create_stack(stack_name, heat_template, heat_inputs)
        return CreateInfrastructureResponse(stack_id, stack_id)

    def get_infrastructure_task(self, infrastructure_id, request_id, deployment_location):
        openstack_location = self.location_translator.from_deployment_location(deployment_location)
        heat_driver = openstack_location.heat_driver
        try:
            stack = heat_driver.get_stack(infrastructure_id)
        except StackNotFoundError as e:
            logger.debug('Stack not found: %s', infrastructure_id)
            if request_id.startswith(DELETE_REQUEST_PREFIX):
                logger.debug('Stack not found on delete request, returning task as successful: %s', infrastructure_id)
                return InfrastructureTask(infrastructure_id, request_id, STATUS_COMPLETE, None, {})
            else:
                raise InfrastructureNotFoundError(str(e)) from e
        logger.debug('Retrieved stack: %s', stack)
        return self.__build_infrastructure_response(stack, request_id)

    def delete_infrastructure(self, infrastructure_id, deployment_location):
        openstack_location = self.location_translator.from_deployment_location(deployment_location)
        heat_driver = openstack_location.heat_driver
        try:
            heat_driver.delete_stack(infrastructure_id)
        except StackNotFoundError as e:
            # This is fine, as we want the stack to be deleted. 
            # Return a response so the monitor calls get_infrastructure_task which will return the correct async result
            pass
        return DeleteInfrastructureResponse(infrastructure_id, DELETE_REQUEST_PREFIX+infrastructure_id)

    def find_infrastructure(self, template, template_type, instance_name, deployment_location):
        if template_type.upper() != TOSCA_TEMPLATE_TYPE.upper():
            raise InvalidInfrastructureTemplateError('Cannot find by template_type \'{0}\'. Must be \'{1}\''.format(template_type, TOSCA_TEMPLATE_TYPE))
        openstack_location = self.location_translator.from_deployment_location(deployment_location)
        inputs = {
            'instance_name': instance_name
        }
        find_result = None
        try:
            discover_result = self.tosca_discovery_service.discover(template, openstack_location, inputs)
            find_result = FindInfrastructureResult(discover_result.discover_id, discover_result.outputs)
        except NotDiscoveredError as e:
            pass  # Return empty result
        except ToscaValidationError as e:
            raise InvalidInfrastructureTemplateError(str(e)) from e
        return FindInfrastructureResponse(find_result)

    def __build_infrastructure_response(self, stack, request_id):
        infrastructure_id = stack.get('id')
        stack_status = stack.get('stack_status', None)
        failure_details = None
        if stack_status in [OS_STACK_STATUS_CREATE_IN_PROGRESS, OS_STACK_STATUS_DELETE_IN_PROGRESS, OS_STACK_STATUS_ADOPT_IN_PROGRESS]:
            logger.debug('Stack %s has stack_status %s, setting status in response to %s', infrastructure_id, stack_status, STATUS_IN_PROGRESS)
            status = STATUS_IN_PROGRESS
        elif stack_status in [OS_STACK_STATUS_CREATE_COMPLETE, OS_STACK_STATUS_DELETE_COMPLETE, OS_STACK_STATUS_ADOPT_COMPLETE]:
            logger.debug('Stack %s has stack_status %s, setting status in response to %s', infrastructure_id, stack_status, STATUS_COMPLETE)
            status = STATUS_COMPLETE
        elif stack_status in [OS_STACK_STATUS_CREATE_FAILED, OS_STACK_STATUS_DELETE_FAILED, OS_STACK_STATUS_ADOPT_FAILED]:
            logger.debug('Stack %s has stack_status %s, setting status in response to %s', infrastructure_id, stack_status, STATUS_FAILED)
            status = STATUS_FAILED
            description = stack.get('stack_status_reason', None)
            failure_details = FailureDetails(FAILURE_CODE_INFRASTRUCTURE_ERROR, description)
            status_reason = stack.get('stack_status_reason', None)
        else:
            logger.debug('Stack %s has stack_status %s, setting status in response to %s', infrastructure_id, stack_status, STATUS_UNKNOWN)
            status = STATUS_UNKNOWN
        is_create = True
        if stack_status in [OS_STACK_STATUS_DELETE_IN_PROGRESS, OS_STACK_STATUS_DELETE_COMPLETE, OS_STACK_STATUS_DELETE_FAILED]:
            is_create = False
        outputs = None
        if is_create:
            logger.debug('Stack %s last process is a create', infrastructure_id)
            outputs_from_stack = stack.get('outputs', [])
            outputs = self.__translate_outputs_to_values_dict(outputs_from_stack)
        return InfrastructureTask(infrastructure_id, request_id, status, failure_details, outputs)

    def __translate_outputs_to_values_dict(self, stack_outputs):
        if len(stack_outputs) == 0:
            return None
        outputs = {}
        for stack_output in stack_outputs:
            key = stack_output.get('output_key')
            value = stack_output.get('output_value')
            outputs[key] = value
        return outputs
