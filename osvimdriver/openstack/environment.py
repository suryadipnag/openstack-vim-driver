from keystoneauth1.identity import v3 as keystonev3
from keystoneauth1 import session as keystonesession
from osvimdriver.openstack.heat.driver import HeatDriver
from osvimdriver.openstack.heat.template import HeatInputUtil
from osvimdriver.openstack.neutron.driver import NeutronDriver

AUTH_PROP_PREFIX = 'os_auth_'
AUTH_ENABLED_PROP = 'os_auth_enabled'
AUTH_API_PROP = 'os_auth_api'
OS_URL_PROP = 'os_api_url'


class OpenstackPasswordAuth():

    def __init__(self, auth_api, auth_properties={}):
        if auth_api is None:
            raise ValueError('auth_api must be set')
        self.auth_api = auth_api
        self.auth_properties = auth_properties

    def build_os_auth(self, api_url):
        full_auth_url = api_url + '/' + self.auth_api
        full_auth_props = self.auth_properties.copy()
        full_auth_props['auth_url'] = full_auth_url
        auth = keystonev3.Password(**full_auth_props)
        return auth


class OpenstackDeploymentLocation():

    def __init__(self, name, api_url, auth):
        self.name = name
        self.__api_url = api_url
        self.__auth = auth
        self.__session = None
        self.__heat_driver = None
        self.__neutron_driver = None

    def create_session(self):
        auth_details = self.__auth.build_os_auth(self.__api_url) if self.__auth is not None else None
        self.__session = keystonesession.Session(auth=auth_details)
        return self.__session

    def get_session(self):
        if self.__session is None:
            self.create_session()
        return self.__session

    @property
    def heat_driver(self):
        if self.__heat_driver is None:
            self.__heat_driver = HeatDriver(self.get_session())
        return self.__heat_driver

    def get_heat_input_util(self):
        return HeatInputUtil()

    @property
    def neutron_driver(self):
        if self.__neutron_driver is None:
            self.__neutron_driver = NeutronDriver(self.get_session())
        return self.__neutron_driver


class OpenstackDeploymentLocationTranslator():

    def from_deployment_location(self, deployment_location):
        dl_name = deployment_location.get('name')
        if dl_name is None:
            raise ValueError('Deployment Location managed by the Openstack VIM Driver must have a name')
        dl_properties = deployment_location.get('properties', {})
        # Get Openstack URL
        api_url = dl_properties.get(OS_URL_PROP, None)
        if api_url is None:
            raise ValueError('Deployment Location managed by the Openstack VIM Driver must specify a property value for \'{0}\''.format(OS_URL_PROP))
        # Gather auth properties
        auth_enabled = True
        auth_api = None
        auth_properties = {}
        for key, value in dl_properties.items():
            if key == AUTH_ENABLED_PROP:
                if isinstance(value, bool):
                    auth_enabled = value
                else:
                    raise ValueError('Deployment Location should have a boolean value for property \'{0}\''.format(AUTH_ENABLED_PROP))
            elif key == AUTH_API_PROP:
                auth_api = value
            elif key.startswith(AUTH_PROP_PREFIX):
                auth_prop_key = key[len(AUTH_PROP_PREFIX):]
                auth_properties[auth_prop_key] = value
        if auth_enabled:
            if auth_api is None:
                raise ValueError('Deployment Location must specify a value for property \'{0}\' when auth is enabled'.format(AUTH_API_PROP))
            configured_auth = OpenstackPasswordAuth(auth_api, auth_properties)
        else:
            configured_auth = None
        return OpenstackDeploymentLocation(dl_name, api_url, configured_auth)
