from translator.hot.tosca.etsi_nfv.tosca_nfv_vducp import ToscaNfvVducp

TARGET_CLASS_NAME = 'OSNfvVducp'

CUSTOM_PROPS = ['admin_state_up', 'allowed_address_pairs', 'device_id', 'device_owner', 'dns_name', 'fixed_ips', 'mac_address' \
                    'port_security_enabled', 'qos_policy', 'security_groups', 'tags', 'value_specs']


class OSNfvVducp(ToscaNfvVducp):
    """Translate TOSCA node type tosca.nodes.nfv.VduCp.NeutronPort, an extension to tosca.nodes.nfv.VduCp"""

    toscatype = 'tosca.nodes.nfv.VduCp.NeutronPort'

    def __is_custom_prop(self, prop_name):
        return prop_name in CUSTOM_PROPS

    def handle_properties(self):
        super(OSNfvVducp, self).handle_properties()     

        if self.virtual_link and 'network' in self.properties:
            network_node_name = self.virtual_link
            # Check network is in the topology otherwise override the use of "get_resource"
            match = None
            for node_name, node_tpl in self.nodetemplate.templates.items():
                if node_name == network_node_name:
                    match = node_tpl
                    break
            if match == None:
                self.properties['network'] = network_node_name
            else:
                match_props = match.get('properties', {})
                if len(match_props) == 1 and 'name' in match_props:
                    self.properties['network'] = match_props.get('name')

        tosca_props = self.get_tosca_props()
        for key, value in tosca_props.items():
            if key == 'security_groups':
                if isinstance(value, list):
                    new_value = []
                    for e in value:
                        found_match = False
                        for node_name, _ in self.nodetemplate.templates.items():
                            if node_name == e:
                                found_match = True
                                break
                        if found_match:
                            new_value.append({'get_resource': e})
                        else:
                            new_value.append(e)
                    self.properties[key] = new_value
                else:
                    self.properties[key] = value
            elif self.__is_custom_prop(key):
                self.properties[key] = value

    def get_hot_attribute(self, attribute, args):
        if attribute == 'ip_address':
            attr = {}
            attr['get_attr'] = [self.name, 'fixed_ips', '0', 'ip_address']
            return attr
        elif attribute in CUSTOM_PROPS:
            attr = {}
            attr['get_attr'] = [self.name, attribute]
            return attr
        return super(OSNfvVducp, self).get_hot_attribute(attribute, args)

