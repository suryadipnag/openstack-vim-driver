from translator.hot.syntax.hot_resource import HotResource

TARGET_CLASS_NAME = 'OSNfvVnfVirtualLink'
HOT_TYPE = 'OS::Neutron::Net'

CUSTOM_PROPS = ['admin_state_up', 'dhcp_agent_ids', 'dns_domain', 'port_security_enabled', 'qos_policy', \
                    'shared', 'tags', 'tenant_id', 'value_specs']

class OSNfvVnfVirtualLink(HotResource):
    """Translate TOSCA node type tosca.nodes.nfv.VnfVirtualLink.NeutronNetwork, an extension to tosca.nodes.nfv.VnfVirtualLink"""

    toscatype = 'tosca.nodes.nfv.VnfVirtualLink.NeutronNetwork'

    def __init__(self, nodetemplate, csar_dir=None):
        # Check if it refers to an existing Network by name
        self.network_name = None
        if len(nodetemplate.get_properties_objects()) == 1 and nodetemplate.get_properties_objects()[0].name == 'name':
            self.network_name = nodetemplate.get_properties_objects()[0].value

        if self.network_name is None:
            super(OSNfvVnfVirtualLink, self).__init__(nodetemplate, csar_dir=csar_dir)
        else:
            # We're customising the translation
            super(OSNfvVnfVirtualLink, self).__init__(nodetemplate, type=HOT_TYPE, csar_dir=csar_dir)
            self.hide_resource = True
            self.existing_resource_id = self.network_name

    def __is_custom_prop(self, prop_name):
        return prop_name in CUSTOM_PROPS

    def handle_properties(self):
        if self.network_name is not None:
            self.properties = {'name': self.network_name}
        else:
            tosca_props = self.get_tosca_props()
            self.properties = {}
            for key, value in tosca_props.items():
                if self.__is_custom_prop(key):
                    self.properties[key] = value

    def handle_expansion(self):
        return []

    def get_hot_attribute(self, attribute, args):
        if attribute in CUSTOM_PROPS:
            attr = {}
            attr['get_attr'] = [self.name, attribute]
            return attr
        return super().get_hot_attribute(attribute, args)

            