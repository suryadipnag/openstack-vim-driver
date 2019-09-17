import uuid
import logging
from ignition.service.framework import Service, Capability, interface
from ignition.service.infrastructure import InfrastructureDriverCapability, InfrastructureNotFoundError, InvalidInfrastructureTemplateError
from ignition.model.infrastructure import CreateInfrastructureResponse, DeleteInfrastructureResponse, FindInfrastructureResponse, InfrastructureTask, STATUS_IN_PROGRESS, STATUS_COMPLETE, STATUS_FAILED, STATUS_UNKNOWN
from ignition.model.failure import FailureDetails, FAILURE_CODE_INFRASTRUCTURE_ERROR
from osvimdriver.service.tosca import ToscaValidationError, NotDiscoveredError
from osvimdriver.openstack.heat.driver import StackNotFoundError

logger = logging.getLogger(__name__)

OS_STACK_STATUS_CREATE_IN_PROGRESS = 'CREATE_IN_PROGRESS'
OS_STACK_STATUS_CREATE_COMPLETE = 'CREATE_COMPLETE'
OS_STACK_STATUS_CREATE_FAILED = 'CREATE_FAILED'
OS_STACK_STATUS_DELETE_IN_PROGRESS = 'DELETE_IN_PROGRESS'
OS_STACK_STATUS_DELETE_COMPLETE = 'DELETE_COMPLETE'
OS_STACK_STATUS_DELETE_FAILED = 'DELETE_FAILED'


class InfrastructureDriver(Service, InfrastructureDriverCapability):

    def __init__(self, location_translator, **kwargs):
        if 'heat_translator_service' not in kwargs:
            raise ValueError('heat_translator_service argument not provided')
        self.heat_translator = kwargs.get('heat_translator_service')
        if 'tosca_discovery_service' not in kwargs:
            raise ValueError('tosca_discovery_service argument not provided')
        self.tosca_discovery_service = kwargs.get('tosca_discovery_service')
        self.location_translator = location_translator

    def create_infrastructure(self, template, inputs, deployment_location):
        try:
            heat_template = self.heat_translator.generate_heat_template(template)
        except ToscaValidationError as e:
            raise InvalidInfrastructureTemplateError(str(e)) from e
        logger.debug('Translated Tosca template:\n%s\nto Heat template:\n%s', template, heat_template)
        openstack_location = self.location_translator.from_deployment_location(deployment_location)
        heat_driver = openstack_location.heat_driver
        heat_input_util = openstack_location.get_heat_input_util()
        heat_inputs = heat_input_util.filter_used_properties(heat_template, inputs)
        stack_name = 's' + uuid.uuid4().hex
        stack_id = heat_driver.create_stack(stack_name, heat_template, heat_inputs)
        return CreateInfrastructureResponse(stack_id, stack_id)

    def get_infrastructure_task(self, infrastructure_id, request_id, deployment_location):
        openstack_location = self.location_translator.from_deployment_location(deployment_location)
        heat_driver = openstack_location.heat_driver
        try:
            stack = heat_driver.get_stack(infrastructure_id)
        except StackNotFoundError as e:
            raise InfrastructureNotFoundError(str(e)) from e
        logger.debug('Retrieved stack: %s', stack)
        return self.__build_infrastructure_response(stack)

    def delete_infrastructure(self, infrastructure_id, deployment_location):
        openstack_location = self.location_translator.from_deployment_location(deployment_location)
        heat_driver = openstack_location.heat_driver
        heat_driver.delete_stack(infrastructure_id)
        return DeleteInfrastructureResponse(infrastructure_id, infrastructure_id)

    def find_infrastructure(self, template, instance_name, deployment_location):
        openstack_location = self.location_translator.from_deployment_location(deployment_location)
        inputs = {
            'instance_name': instance_name
        }
        try:
            discover_result = self.tosca_discovery_service.discover(template, openstack_location, inputs)
        except NotDiscoveredError as e:
            raise InfrastructureNotFoundError(str(e)) from e
        except ToscaValidationError as e:
            raise InvalidInfrastructureTemplateError(str(e)) from e
        return FindInfrastructureResponse(discover_result.discover_id, discover_result.outputs)

    def __build_infrastructure_response(self, stack):
        infrastructure_id = stack.get('id')
        stack_status = stack.get('stack_status', None)
        failure_details = None
        if stack_status in [OS_STACK_STATUS_CREATE_IN_PROGRESS, OS_STACK_STATUS_DELETE_IN_PROGRESS]:
            logger.debug('Stack %s has stack_status %s, setting status in response to %s', infrastructure_id, stack_status, STATUS_IN_PROGRESS)
            status = STATUS_IN_PROGRESS
        elif stack_status in [OS_STACK_STATUS_CREATE_COMPLETE, OS_STACK_STATUS_DELETE_COMPLETE]:
            logger.debug('Stack %s has stack_status %s, setting status in response to %s', infrastructure_id, stack_status, STATUS_COMPLETE)
            status = STATUS_COMPLETE
        elif stack_status in [OS_STACK_STATUS_CREATE_FAILED, OS_STACK_STATUS_DELETE_FAILED]:
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
        return InfrastructureTask(infrastructure_id, infrastructure_id, status, failure_details, outputs)

    def __translate_outputs_to_values_dict(self, stack_outputs):
        if len(stack_outputs) == 0:
            return None
        outputs = {}
        for stack_output in stack_outputs:
            key = stack_output.get('output_key')
            value = stack_output.get('output_value')
            outputs[key] = value
        return outputs
