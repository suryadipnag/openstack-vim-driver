import uuid
import logging
import re
from ignition.service.framework import Service, Capability, interface
from ignition.service.resourcedriver import ResourceDriverHandlerCapability, InfrastructureNotFoundError, InvalidDriverFilesError, ResourceDriverError, InvalidRequestError
from ignition.model.references import FindReferenceResponse, FindReferenceResult
from ignition.model.associated_topology import AssociatedTopology
from ignition.model.lifecycle import LifecycleExecuteResponse, LifecycleExecution, STATUS_IN_PROGRESS, STATUS_COMPLETE, STATUS_FAILED, STATUS_UNKNOWN
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

REQUEST_ID_SEPARATOR = '::'
CREATE_REQUEST_PREFIX = 'Create'
DELETE_REQUEST_PREFIX = 'Delete'

STACK_RESOURCE_TYPE = 'Openstack.Stack'
STACK_NAME = 'InfrastructureStack'

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

class ResourceDriverHandler(Service, ResourceDriverHandlerCapability):

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
    
    def execute_lifecycle(self, lifecycle_name, driver_files, system_properties, resource_properties, request_properties, internal_resources, deployment_location):
        try:
            openstack_location = self.location_translator.from_deployment_location(deployment_location)
            if lifecycle_name.upper() == 'CREATE':
                return self.__handle_create(driver_files, system_properties, resource_properties, request_properties, internal_resources, openstack_location)
            elif lifecycle_name.upper() == 'DELETE':
                return self.__handle_delete(driver_files, system_properties, resource_properties, request_properties, internal_resources, openstack_location)
            else:
                raise InvalidRequestError(f'Openstack driver only supports Create and Delete transitions, not {lifecycle_name}')
        finally:
            try:
                logger.debug(f'Attempting to remove driver files at {driver_files.root_path}')
                driver_files.remove_all()
            except Exception as e:
                logger.exception('Encountered an error whilst trying to clear out driver files directory {0}: {1}'.format(driver_files.root_path, str(e)))

    def __handle_create(self, driver_files, system_properties, resource_properties, request_properties, internal_resources, openstack_location):
        heat_driver = openstack_location.heat_driver
        stack_id = None
        if 'stack_id' in resource_properties:
            input_stack_id = resource_properties.get('stack_id')
            if input_stack_id != None and len(input_stack_id.strip())!=0 and input_stack_id.strip() != "0":
                try:
                    ##Check for valid stack
                    heat_driver.get_stack(input_stack_id.strip())
                except StackNotFoundError as e:
                    raise InfrastructureNotFoundError(str(e)) from e
                else:
                    stack_id = input_stack_id
        if stack_id is None:
            template_type = request_properties.get('template-type', None)
            if template_type is not None and template_type.upper() == TOSCA_TEMPLATE_TYPE.upper():
                heat_template = self.__get_heat_template_from_tosca(driver_files)
            elif template_type is None or template_type.upper() == HEAT_TEMPLATE_TYPE.upper():
                heat_template = self.__get_heat_template(driver_files)
            else:
                raise InvalidDriverFilesError('Cannot create using template of type \'{0}\'. Must be one of: {1}'.format(template_type, [TOSCA_TEMPLATE_TYPE, HEAT_TEMPLATE_TYPE]))
            heat_input_util = openstack_location.get_heat_input_util()
            input_props = self.props_merger.merge(resource_properties, system_properties)
            heat_inputs = heat_input_util.filter_used_properties(heat_template, input_props)
            if 'resourceId' in system_properties and 'resourceName' in system_properties:
                stack_name = self.stack_name_creator.create(system_properties['resourceId'], system_properties['resourceName'])
            else:
                stack_name = 's' + str(uuid.uuid4())
            stack_id = heat_driver.create_stack(stack_name, heat_template, heat_inputs)
        request_id = self.__build_request_id(CREATE_REQUEST_PREFIX, stack_id)
        internal_resources = self.__build_internal_resources_response(stack_id)
        return LifecycleExecuteResponse(request_id, internal_resources=internal_resources)

    def __handle_delete(self, driver_files, system_properties, resource_properties, request_properties, internal_resources, openstack_location):
        stack_resource_entry = internal_resources.get_by_name(STACK_NAME)
        if stack_resource_entry is None:
            # There is no Stack associated to this Resource
            # This is fine, as we want the stack to be deleted. 
            # Return a response so the monitor calls get_lifecycle_execution which will return the correct async result
            request_id = self.__build_request_id(DELETE_REQUEST_PREFIX, 'no-stack')
        else:
            stack_id = stack_resource_entry.identifier
            heat_driver = openstack_location.heat_driver
            try:
                heat_driver.delete_stack(stack_id)
            except StackNotFoundError as e:
                # This is fine, as we want the stack to be deleted. 
                # Return a response so the monitor calls get_lifecycle_execution which will return the correct async result
                pass
            request_id = self.__build_request_id(DELETE_REQUEST_PREFIX, stack_id)
        return LifecycleExecuteResponse(request_id)

    def find_reference(self, instance_name, driver_files, deployment_location):
        openstack_location = self.location_translator.from_deployment_location(deployment_location)
        inputs = {
            'instance_name': instance_name
        }
        template = self.__get_discover_template(driver_files)
        find_result = None
        try:
            discover_result = self.tosca_discovery_service.discover(template, openstack_location, inputs)
            find_result = FindReferenceResult(discover_result.discover_id, discover_result.outputs)
        except NotDiscoveredError as e:
            pass  # Return empty result
        except ToscaValidationError as e:
            raise InvalidDriverFilesError(str(e)) from e
        return FindReferenceResponse(find_result)

    def __build_request_id(self, request_type, stack_id):
        request_id = request_type
        request_id += REQUEST_ID_SEPARATOR
        request_id += stack_id
        request_id += REQUEST_ID_SEPARATOR
        request_id += str(uuid.uuid4())
        return request_id 

    def __split_request_id(self, request_id):
        split_parts = request_id.split(REQUEST_ID_SEPARATOR)
        if len(split_parts) != 3:
            raise InvalidRequestError(f'request_id is not valid: {request_id}')
        request_type = split_parts[0]
        stack_id = split_parts[1]
        operation_id = split_parts[2]
        return (request_type, stack_id, operation_id)

    def __build_internal_resources_response(self, stack_id):
        internal_resources = AssociatedTopology()
        internal_resources.add_entry(stack_id, STACK_NAME, STACK_RESOURCE_TYPE)
        return internal_resources

    def __get_discover_template(self, driver_files):
        if driver_files.has_file('discover.yaml'):
            template_path = driver_files.get_file_path('discover.yaml')
        elif driver_files.has_file('discover.yml'):
            template_path = driver_files.get_file_path('discover.yml')
        else:
            raise InvalidDriverFilesError('Missing \'discover.yaml\' or \'discover.yml\' file')
        with open(template_path, 'r') as f:
            template = f.read()
        return template

    def __get_heat_template_from_tosca(self, driver_files):
        if driver_files.has_file('tosca.yaml'):
            template_path = driver_files.get_file_path('tosca.yaml')
        elif driver_files.has_file('tosca.yml'):
            template_path = driver_files.get_file_path('tosca.yml')
        else:
            raise InvalidDriverFilesError('Missing \'tosca.yaml\' or \'tosca.yml\' file')
        with open(template_path, 'r') as f:
            template = f.read()
        try:
            heat_template = self.heat_translator.generate_heat_template(template)
        except ToscaValidationError as e:
            raise InvalidDriverFilesError(str(e)) from e
        logger.debug('Translated Tosca template:\n%s\nto Heat template:\n%s', template, heat_template)
        return heat_template

    def __get_heat_template(self, driver_files):
        if driver_files.has_file('heat.yaml'):
            template_path = driver_files.get_file_path('heat.yaml')
        elif driver_files.has_file('heat.yml'):
            template_path = driver_files.get_file_path('heat.yml')
        else:
            raise InvalidDriverFilesError('Missing \'heat.yaml\' or \'heat.yml\' file')
        with open(template_path, 'r') as f:
            heat_template = f.read()
        return heat_template

    def get_lifecycle_execution(self, request_id, deployment_location):
        openstack_location = self.location_translator.from_deployment_location(deployment_location)
        heat_driver = openstack_location.heat_driver
        request_type, stack_id, operation_id = self.__split_request_id(request_id)
        try:
            stack = heat_driver.get_stack(stack_id)
        except StackNotFoundError as e:
            logger.debug('Stack not found: %s', stack_id)
            if request_type == DELETE_REQUEST_PREFIX:
                logger.debug('Stack not found on delete request, returning task as successful: %s', stack_id)
                return LifecycleExecution(request_id, STATUS_COMPLETE)
            else:
                raise InfrastructureNotFoundError(str(e)) from e
        logger.debug('Retrieved stack: %s', stack)
        return self.__build_execution_response(stack, request_id)

    def __build_execution_response(self, stack, request_id):
        request_type, stack_id, operation_id = self.__split_request_id(request_id)
        stack_status = stack.get('stack_status', None)
        failure_details = None
        if request_type == CREATE_REQUEST_PREFIX:
            status = self.__determine_create_status(request_id, stack_id, stack_status)
        else:
            status = self.__determine_delete_status(request_id, stack_id, stack_status)
        if status == STATUS_FAILED:
            description = stack.get('stack_status_reason', None)
            failure_details = FailureDetails(FAILURE_CODE_INFRASTRUCTURE_ERROR, description)
            status_reason = stack.get('stack_status_reason', None)
        outputs = None
        internal_resources = None
        if request_type == CREATE_REQUEST_PREFIX:
            outputs_from_stack = stack.get('outputs', [])
            outputs = self.__translate_outputs_to_values_dict(outputs_from_stack)
        return LifecycleExecution(request_id, status, failure_details=failure_details, outputs=outputs)

    def __determine_create_status(self, request_id, stack_id, stack_status):
        if stack_status in [OS_STACK_STATUS_CREATE_IN_PROGRESS, OS_STACK_STATUS_ADOPT_IN_PROGRESS]:
            create_status = STATUS_IN_PROGRESS
        elif stack_status in [OS_STACK_STATUS_CREATE_COMPLETE, OS_STACK_STATUS_ADOPT_COMPLETE]:
            create_status = STATUS_COMPLETE
        elif stack_status in [OS_STACK_STATUS_CREATE_FAILED, OS_STACK_STATUS_ADOPT_FAILED]:
            create_status = STATUS_FAILED
        else:
            raise ResourceDriverError(f'Cannot determine status for request \'{request_id}\' as the current Stack status is \'{stack_status}\' which is not a valid value for the expected transition')
        logger.debug('Stack %s has stack_status %s, setting status in response to %s', stack_id, stack_status, create_status)
        return create_status

    def __determine_delete_status(self, request_id, stack_id, stack_status):
        if stack_status in [OS_STACK_STATUS_DELETE_IN_PROGRESS]:
            delete_status = STATUS_IN_PROGRESS
        elif stack_status in [OS_STACK_STATUS_DELETE_COMPLETE]:
            delete_status = STATUS_COMPLETE
        elif stack_status in [OS_STACK_STATUS_DELETE_FAILED]:
            delete_status = STATUS_FAILED
        else:
            raise ResourceDriverError(f'Cannot determine status for request \'{request_id}\' as the current Stack status is \'{stack_status}\' which is not a valid value for the expected transition')
        logger.debug('Stack %s has stack_status %s, setting status in response to %s', stack_id, stack_status, delete_status)
        return delete_status

    def __translate_outputs_to_values_dict(self, stack_outputs):
        if len(stack_outputs) == 0:
            return None
        outputs = {}
        for stack_output in stack_outputs:
            key = stack_output.get('output_key')
            value = stack_output.get('output_value')
            outputs[key] = value
        return outputs
