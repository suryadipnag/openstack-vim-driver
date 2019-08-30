import unittest
from unittest.mock import patch, MagicMock
from osvimdriver.openstack.neutron.driver import NeutronDriver
from neutronclient.common import exceptions as neutronexceptions


class TestNeutronDriver(unittest.TestCase):

    @patch('osvimdriver.openstack.neutron.driver.neutronclient.Client')
    def test_get_network_by_id(self, mock_neutron_client_init):
        mock_neutron_client = mock_neutron_client_init.return_value
        mock_neutron_client.show_network.return_value = {'network': {'id': 'mock_network_id'}}
        mock_session = MagicMock()
        neutron_driver = NeutronDriver(mock_session)
        network = neutron_driver.get_network_by_id('mock_network_id')
        mock_neutron_client.show_network.assert_called_once_with('mock_network_id')
        self.assertEqual(network, {'id': 'mock_network_id'})

    @patch('osvimdriver.openstack.neutron.driver.neutronclient.Client')
    def test_get_network_by_id_without_id_fails(self, mock_neutron_client_init):
        mock_session = MagicMock()
        neutron_driver = NeutronDriver(mock_session)
        with self.assertRaises(ValueError) as context:
            neutron_driver.get_network_by_id(None)
        self.assertEqual(str(context.exception), 'network_id must be provided')

    @patch('osvimdriver.openstack.neutron.driver.neutronclient.Client')
    def test_get_network_by_name(self, mock_neutron_client_init):
        mock_neutron_client = mock_neutron_client_init.return_value
        mock_neutron_client.list_networks.return_value = {'networks': [{'name': 'networkA'}, {'name': 'networkB'}]}
        mock_session = MagicMock()
        neutron_driver = NeutronDriver(mock_session)
        network = neutron_driver.get_network_by_name('networkB')
        mock_neutron_client.list_networks.assert_called_once()
        self.assertEqual(network, {'name': 'networkB'})

    @patch('osvimdriver.openstack.neutron.driver.neutronclient.Client')
    def test_get_network_by_name_without_name_fails(self, mock_neutron_client_init):
        mock_session = MagicMock()
        neutron_driver = NeutronDriver(mock_session)
        with self.assertRaises(ValueError) as context:
            neutron_driver.get_network_by_name(None)
        self.assertEqual(str(context.exception), 'network_name must be provided')

    @patch('osvimdriver.openstack.neutron.driver.neutronclient.Client')
    def test_get_network_by_name_not_unique_result_fails(self, mock_neutron_client_init):
        mock_neutron_client = mock_neutron_client_init.return_value
        mock_neutron_client.list_networks.return_value = {'networks': [{'name': 'networkA'}, {'name': 'networkA'}]}
        mock_session = MagicMock()
        neutron_driver = NeutronDriver(mock_session)
        with self.assertRaises(neutronexceptions.NeutronClientNoUniqueMatch) as context:
            neutron_driver.get_network_by_name('networkA')
        self.assertEqual(str(context.exception), 'Multiple Network matches found for name \'networkA\', use an ID to be more specific.')

    @patch('osvimdriver.openstack.neutron.driver.neutronclient.Client')
    def test_get_network_by_name_not_found_fails(self, mock_neutron_client_init):
        mock_neutron_client = mock_neutron_client_init.return_value
        mock_neutron_client.list_networks.return_value = {'networks': [{'name': 'networkA'}]}
        mock_session = MagicMock()
        neutron_driver = NeutronDriver(mock_session)
        with self.assertRaises(neutronexceptions.NotFound) as context:
            neutron_driver.get_network_by_name('networkB')
        self.assertEqual(str(context.exception), 'Unable to find network with name \'networkB\'')

    @patch('osvimdriver.openstack.neutron.driver.neutronclient.Client')
    def test_get_subnet_by_id(self, mock_neutron_client_init):
        mock_neutron_client = mock_neutron_client_init.return_value
        mock_neutron_client.show_subnet.return_value = {'subnet': {'id': 'mock_subnet_id'}}
        mock_session = MagicMock()
        neutron_driver = NeutronDriver(mock_session)
        subnet = neutron_driver.get_subnet_by_id('mock_subnet_id')
        mock_neutron_client.show_subnet.assert_called_once_with('mock_subnet_id')
        self.assertEqual(subnet, {'id': 'mock_subnet_id'})

    @patch('osvimdriver.openstack.neutron.driver.neutronclient.Client')
    def test_get_subnet_by_id_without_id_fails(self, mock_neutron_client_init):
        mock_session = MagicMock()
        neutron_driver = NeutronDriver(mock_session)
        with self.assertRaises(ValueError) as context:
            neutron_driver.get_subnet_by_id(None)
        self.assertEqual(str(context.exception), 'subnet_id must be provided')
