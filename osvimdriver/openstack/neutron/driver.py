import logging
from neutronclient.v2_0 import client as neutronclient
from neutronclient.common import exceptions as neutronexceptions

logger = logging.getLogger(__name__)


class NeutronDriver():

    def __init__(self, session):
        self.__session = session
        self.__neutron_client = neutronclient.Client(session=self.__session)

    def __get_neutron_client(self):
        return self.__neutron_client

    def get_network_by_id(self, network_id):
        if network_id is None:
            raise ValueError('network_id must be provided')
        neutron_client = self.__get_neutron_client()
        logger.debug('Retrieving network with id %s', network_id)
        result = neutron_client.show_network(network_id)
        return result['network']

    def get_network_by_name(self, network_name):
        if network_name is None:
            raise ValueError('network_name must be provided')
        neutron_client = self.__get_neutron_client()
        logger.debug('Retrieving network with name %s', network_name)
        result = neutron_client.list_networks()
        matches = []
        for network in result['networks']:
            if network['name'] == network_name:
                matches.append(network)
        if len(matches) > 1:
            raise neutronexceptions.NeutronClientNoUniqueMatch(resource='Network',
                                                               name=network_name)
        elif len(matches) == 1:
            return matches[0]
        else:
            raise neutronexceptions.NotFound(message='Unable to find network with name \'{0}\''.format(network_name))

    def get_subnet_by_id(self, subnet_id):
        if subnet_id is None:
            raise ValueError('subnet_id must be provided')
        neutron_client = self.__get_neutron_client()
        logger.debug('Retrieving subnet with id %s', subnet_id)
        result = neutron_client.show_subnet(subnet_id)
        return result['subnet']
