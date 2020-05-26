import logging
from heatclient import client as heatclient
from heatclient import exc as heatexc

logger = logging.getLogger(__name__)


class StackNotFoundError(Exception):
    pass


class HeatDriver():

    def __init__(self, session):
        self.__session = session
        self.__heat_client = heatclient.Client('1', session=self.__session)

    def __get_heat_client(self):
        return self.__heat_client

    def create_stack(self, stack_name, heat_template, input_properties=None, files=None):
        if input_properties is None:
            input_properties = {}
        if files is None:
            files = {}
        if stack_name is None:
            raise ValueError('stack_name must be provided')
        if heat_template is None:
            raise ValueError('heat_template must be provided')
        heat_client = self.__get_heat_client()
        logger.debug('Creating stack with name %s', stack_name)
        create_result = heat_client.stacks.create(stack_name=stack_name, template=heat_template, parameters=input_properties, files=files)
        stack_id = create_result['stack']['id']
        logger.debug('Stack with name %s created and assigned id %s', stack_name, stack_id)
        return stack_id

    def delete_stack(self, stack_id):
        if stack_id is None:
            raise ValueError('stack_id must be provided')
        heat_client = self.__get_heat_client()
        logger.debug('Deleting stack with id %s', stack_id)
        try:
            delete_result = heat_client.stacks.delete(stack_id)
        except heatexc.HTTPNotFound as e:
            raise StackNotFoundError(str(e)) from e

    def get_stack(self, stack_id):
        if stack_id is None:
            raise ValueError('stack_id must be provided')
        heat_client = self.__get_heat_client()
        logger.debug('Retrieving stack with id %s', stack_id)
        try:
            result = heat_client.stacks.get(stack_id)
        except heatexc.HTTPNotFound as e:
            raise StackNotFoundError(str(e)) from e
        return result.to_dict()

    def get_stacks(self):
        heat_client = self.__get_heat_client()
        logger.debug('Retrieving stacks %s')
        result = heat_client.stacks.list()
        return result
