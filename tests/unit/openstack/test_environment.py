import os
import unittest
import yaml
import tests.unit.openstack.certs as certs
from osvimdriver.openstack.environment import OpenstackDeploymentLocationTranslator, OpenstackDeploymentLocation, OpenstackPasswordAuth, OS_URL_PROP, AUTH_ENABLED_PROP, AUTH_API_PROP
from unittest.mock import patch, MagicMock


class TestOpenstackPasswordAuth(unittest.TestCase):

    def test_init_missing_auth_api(self):
        with self.assertRaises(ValueError) as context:
            OpenstackPasswordAuth(None, None)
        self.assertEqual(str(context.exception), 'auth_api must be set')

    @patch('osvimdriver.openstack.environment.keystonev3.Password')
    def test_build_os_auth(self, mock_keystone_password_init):
        mock_password = mock_keystone_password_init.return_value
        auth = OpenstackPasswordAuth('identity/v3', auth_properties={'username': 'test', 'password': 'secret'})
        os_auth = auth.build_os_auth('http://testip')
        self.assertEqual(os_auth, mock_password)
        mock_keystone_password_init.assert_called_with(auth_url='http://testip/identity/v3', username='test', password='secret')


class TestOpenstackDeploymentLocation(unittest.TestCase):

    @patch('osvimdriver.openstack.environment.keystonesession.Session')
    def test_create_session(self, mock_keystone_session_init):
        mock_os_auth = MagicMock()
        mock_auth = MagicMock()
        mock_auth.build_os_auth.return_value = mock_os_auth
        mock_keystone_session = mock_keystone_session_init.return_value
        location = OpenstackDeploymentLocation('testdl', 'http://testip', mock_auth)
        session = location.create_session()
        mock_auth.build_os_auth.assert_called_once_with('http://testip')
        mock_keystone_session_init.assert_called_once_with(auth=mock_os_auth)
        self.assertEqual(session, mock_keystone_session)

    @patch('osvimdriver.openstack.environment.keystonesession.Session')
    def test_get_session(self, mock_keystone_session_init):
        mock_os_auth = MagicMock()
        mock_auth = MagicMock()
        mock_auth.build_os_auth.return_value = mock_os_auth
        mock_keystone_session = mock_keystone_session_init.return_value
        location = OpenstackDeploymentLocation('testdl', 'http://testip', mock_auth)
        session = location.get_session()
        mock_auth.build_os_auth.assert_called_once_with('http://testip')
        mock_keystone_session_init.assert_called_once_with(auth=mock_os_auth)
        self.assertEqual(session, mock_keystone_session)

    @patch('osvimdriver.openstack.environment.keystonesession.Session')
    def test_get_session_existing(self, mock_keystone_session_init):
        mock_os_auth = MagicMock()
        mock_auth = MagicMock()
        mock_auth.build_os_auth.return_value = mock_os_auth
        mock_keystone_session = mock_keystone_session_init.return_value
        location = OpenstackDeploymentLocation('testdl', 'http://testip', mock_auth)
        created_session = location.create_session()
        mock_auth.build_os_auth.assert_called_once_with('http://testip')
        mock_keystone_session_init.assert_called_once_with(auth=mock_os_auth)
        get_session = location.get_session()
        self.assertEqual(get_session, created_session)
        mock_auth.build_os_auth.assert_called_once_with('http://testip')
        mock_keystone_session_init.assert_called_once_with(auth=mock_os_auth)

    @patch('osvimdriver.openstack.environment.keystonesession.Session')
    @patch('osvimdriver.openstack.environment.HeatDriver')
    def test_get_heat_driver(self, mock_heat_driver_init, mock_keystone_session_init):
        mock_heat_driver = mock_heat_driver_init.return_value
        mock_auth = MagicMock()
        mock_auth.build_os_auth.return_value = MagicMock()
        location = OpenstackDeploymentLocation('testdl', 'http://testip', mock_auth)
        self.assertIsNone(location._OpenstackDeploymentLocation__session)
        self.assertIsNone(location._OpenstackDeploymentLocation__heat_driver)
        heat_driver = location.heat_driver
        self.assertEqual(heat_driver, mock_heat_driver)
        self.assertEqual(location._OpenstackDeploymentLocation__heat_driver, mock_heat_driver)
        self.assertIsNotNone(location._OpenstackDeploymentLocation__session)

    @patch('osvimdriver.openstack.environment.keystonesession.Session')
    @patch('osvimdriver.openstack.environment.HeatDriver')
    def test_get_heat_driver_existing(self, mock_heat_driver_init, mock_keystone_session_init):
        mock_heat_driver = mock_heat_driver_init.return_value
        mock_auth = MagicMock()
        mock_auth.build_os_auth.return_value = MagicMock()
        location = OpenstackDeploymentLocation('testdl', 'http://testip', mock_auth)
        first_heat_driver = location.heat_driver
        second_heat_driver = location.heat_driver
        self.assertEqual(second_heat_driver, first_heat_driver)

    @patch('osvimdriver.openstack.environment.keystonesession.Session')
    @patch('osvimdriver.openstack.environment.NeutronDriver')
    def test_get_neutron_driver(self, mock_neutron_driver_init, mock_keystone_session_init):
        mock_neutron_driver = mock_neutron_driver_init.return_value
        mock_auth = MagicMock()
        mock_auth.build_os_auth.return_value = MagicMock()
        location = OpenstackDeploymentLocation('testdl', 'http://testip', mock_auth)
        self.assertIsNone(location._OpenstackDeploymentLocation__session)
        self.assertIsNone(location._OpenstackDeploymentLocation__neutron_driver)
        neutron_driver = location.neutron_driver
        self.assertEqual(neutron_driver, mock_neutron_driver)
        self.assertEqual(location._OpenstackDeploymentLocation__neutron_driver, mock_neutron_driver)
        self.assertIsNotNone(location._OpenstackDeploymentLocation__session)

    @patch('osvimdriver.openstack.environment.keystonesession.Session')
    @patch('osvimdriver.openstack.environment.NeutronDriver')
    def test_get_neutron_driver_existing(self, mock_neutron_driver_init, mock_keystone_session_init):
        mock_neutron_driver = mock_neutron_driver_init.return_value
        mock_auth = MagicMock()
        mock_auth.build_os_auth.return_value = MagicMock()
        location = OpenstackDeploymentLocation('testdl', 'http://testip', mock_auth)
        first_neutron_driver = location.neutron_driver
        second_neutron_driver = location.neutron_driver
        self.assertEqual(second_neutron_driver, first_neutron_driver)

    @patch('osvimdriver.openstack.environment.keystonesession.Session')
    def test_get_session_with_certs(self, mock_keystone_session_init):
        mock_os_auth = MagicMock()
        mock_auth = MagicMock()
        mock_auth.build_os_auth.return_value = mock_os_auth
        mock_keystone_session = mock_keystone_session_init.return_value
        certs_dir = os.path.dirname(os.path.abspath(certs.__file__))
        ca_cert_path = os.path.join(certs_dir, 'ca.cert')
        with open(ca_cert_path, 'r') as f:
            ca_cert = f.read()
        client_cert_path = os.path.join(certs_dir, 'client.cert')
        with open(client_cert_path, 'r') as f:
            client_cert = f.read()
        client_key_path = os.path.join(certs_dir, 'client.key')
        with open(client_key_path, 'r') as f:
            client_key = f.read()
        location = OpenstackDeploymentLocation('testdl', 'http://testip', mock_auth, ca_cert=ca_cert, client_cert=client_cert, client_key=client_key)
        try:
            created_session = location.create_session()
            mock_keystone_session_init.assert_called_once_with(auth=mock_os_auth, verify=location._OpenstackDeploymentLocation__ca_cert_path, cert=(location._OpenstackDeploymentLocation__client_cert_path, location._OpenstackDeploymentLocation__client_key_path))
            self.assertTrue(os.path.exists(location._OpenstackDeploymentLocation__ca_cert_path))
            self.assertTrue(os.path.exists(location._OpenstackDeploymentLocation__client_cert_path))
            self.assertTrue(os.path.exists(location._OpenstackDeploymentLocation__client_key_path))
        finally:
            location.close()

    @patch('osvimdriver.openstack.environment.keystonesession.Session')
    def test_close_session_with_certs_removes_files(self, mock_keystone_session_init):
        mock_os_auth = MagicMock()
        mock_auth = MagicMock()
        mock_auth.build_os_auth.return_value = mock_os_auth
        mock_keystone_session = mock_keystone_session_init.return_value
        location = OpenstackDeploymentLocation('testdl', 'http://testip', mock_auth, ca_cert='cacert', client_cert='clientcert', client_key='clientkey')
        try:
            created_session = location.create_session()
            mock_keystone_session_init.assert_called_once_with(auth=mock_os_auth, verify=location._OpenstackDeploymentLocation__ca_cert_path, cert=(location._OpenstackDeploymentLocation__client_cert_path, location._OpenstackDeploymentLocation__client_key_path))
            self.assertTrue(os.path.exists(location._OpenstackDeploymentLocation__ca_cert_path))
            self.assertTrue(os.path.exists(location._OpenstackDeploymentLocation__client_cert_path))
            self.assertTrue(os.path.exists(location._OpenstackDeploymentLocation__client_key_path))
            location.close()
            self.assertFalse(os.path.exists(location._OpenstackDeploymentLocation__ca_cert_path))
            self.assertFalse(os.path.exists(location._OpenstackDeploymentLocation__client_cert_path))
            self.assertFalse(os.path.exists(location._OpenstackDeploymentLocation__client_key_path))
        finally:
            location.close()

class TestOpenstackDeploymentLocationTranslator(unittest.TestCase):

    def test_from_deployment_location_missing_name(self):
        translator = OpenstackDeploymentLocationTranslator()

        with self.assertRaises(ValueError) as context:
            translator.from_deployment_location({'description': 'dl with no name'})
        self.assertEqual(str(context.exception), 'Deployment Location managed by the Openstack VIM Driver must have a name')

    def test_from_deployment_location_missing_properties(self):
        translator = OpenstackDeploymentLocationTranslator()

        with self.assertRaises(ValueError) as context:
            translator.from_deployment_location({'name': 'testdl'})
        self.assertEqual(str(context.exception), 'Deployment Location managed by the Openstack VIM Driver must specify a property value for \'{0}\''.format(OS_URL_PROP))

    def test_from_deployment_location_missing_url(self):
        translator = OpenstackDeploymentLocationTranslator()

        with self.assertRaises(ValueError) as context:
            translator.from_deployment_location({'name': 'testdl', 'properties': {}})
        self.assertEqual(str(context.exception), 'Deployment Location managed by the Openstack VIM Driver must specify a property value for \'{0}\''.format(OS_URL_PROP))

    def test_from_deployment_location_auth_disabled(self):
        translator = OpenstackDeploymentLocationTranslator()
        openstack_location = translator.from_deployment_location({'name': 'testdl', 'properties': {
            OS_URL_PROP: 'testip',
            AUTH_ENABLED_PROP: False
        }})
        self.assertIsNone(openstack_location._OpenstackDeploymentLocation__auth)

    def test_from_deployment_location_auth_enabled_not_a_bool(self):
        translator = OpenstackDeploymentLocationTranslator()
        with self.assertRaises(ValueError) as context:
            translator.from_deployment_location({'name': 'testdl', 'properties': {
                OS_URL_PROP: 'testip',
                AUTH_ENABLED_PROP: 'Truuueee'
            }})
        self.assertEqual(str(context.exception), 'Deployment Location should have a boolean value for property \'{0}\''.format(AUTH_ENABLED_PROP))

    def test_from_deployment_location_auth_api_missing(self):
        translator = OpenstackDeploymentLocationTranslator()
        with self.assertRaises(ValueError) as context:
            translator.from_deployment_location({'name': 'testdl', 'properties': {
                OS_URL_PROP: 'testip'
            }})
        self.assertEqual(str(context.exception), 'Deployment Location must specify a value for property \'{0}\' when auth is enabled'.format(AUTH_API_PROP))

    def test_from_deployment_location_auth_collects_properties_with_prefix(self):
        translator = OpenstackDeploymentLocationTranslator()
        openstack_location = translator.from_deployment_location({'name': 'testdl', 'properties': {
            OS_URL_PROP: 'testip',
            AUTH_API_PROP: 'identity/v3',
            'os_auth_username': 'test',
            'os_auth_password': 'secret',
            'os_auth_domain_id': 'testdomain'
        }})
        self.assertEqual(type(openstack_location._OpenstackDeploymentLocation__auth), OpenstackPasswordAuth)
        openstack_auth = openstack_location._OpenstackDeploymentLocation__auth
        self.assertEqual(openstack_auth.auth_api, 'identity/v3')
        self.assertIn('username', openstack_auth.auth_properties)
        self.assertEqual(openstack_auth.auth_properties['username'], 'test')
        self.assertIn('password', openstack_auth.auth_properties)
        self.assertEqual(openstack_auth.auth_properties['password'], 'secret')
        self.assertIn('domain_id', openstack_auth.auth_properties)
        self.assertEqual(openstack_auth.auth_properties['domain_id'], 'testdomain')
        self.assertEqual(len(openstack_auth.auth_properties), 3)

    def test_from_deployment_location_with_certs(self):
        translator = OpenstackDeploymentLocationTranslator()
        certs_dir = os.path.dirname(os.path.abspath(certs.__file__))
        ca_cert_path = os.path.join(certs_dir, 'ca.cert')
        with open(ca_cert_path, 'r') as f:
            ca_cert = f.read()
        client_cert_path = os.path.join(certs_dir, 'client.cert')
        with open(client_cert_path, 'r') as f:
            client_cert = f.read()
        client_key_path = os.path.join(certs_dir, 'client.key')
        with open(client_key_path, 'r') as f:
            client_key = f.read()
        openstack_location = translator.from_deployment_location({'name': 'testdl', 'properties': {
            OS_URL_PROP: 'testip',
            AUTH_API_PROP: 'identity/v3',
            'os_auth_username': 'test',
            'os_auth_password': 'secret',
            'os_auth_domain_id': 'testdomain',
            'os_cacert': ca_cert,
            'os_cert': client_cert, 
            'os_key': client_key
        }})
        self.assertEqual(openstack_location._OpenstackDeploymentLocation__ca_cert, ca_cert)
        self.assertEqual(openstack_location._OpenstackDeploymentLocation__client_cert, client_cert)
        self.assertEqual(openstack_location._OpenstackDeploymentLocation__client_key, client_key)
    
    @patch('osvimdriver.openstack.environment.keystonesession.Session')
    def test_from_deployment_location_certs_multiline_string(self, mock_keystone_session_init):
        translator = OpenstackDeploymentLocationTranslator()
        certs_dir = os.path.dirname(os.path.abspath(certs.__file__))
        location_path = os.path.join(certs_dir, 'location.yaml')
        with open(location_path, 'r') as f:
            location_dict = yaml.safe_load(f.read())
        location = translator.from_deployment_location(location_dict)
        try:
            location.create_session()
            self.assertTrue(os.path.exists(location._OpenstackDeploymentLocation__ca_cert_path))
            path_to_expected_cacert = os.path.join(certs_dir, 'ca.cert')
            with open(path_to_expected_cacert, 'r') as f:
                expected_cacert = f.read()
            with open(location._OpenstackDeploymentLocation__ca_cert_path, 'r') as f:
                actual_cacert = f.read()
            self.assertEqual(actual_cacert, expected_cacert)
        finally:
            location.close()