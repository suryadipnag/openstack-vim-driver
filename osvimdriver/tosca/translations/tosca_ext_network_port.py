from translator.hot.tosca.tosca_network_port import ToscaNetworkPort

TARGET_CLASS_NAME = 'ToscaExtNetworkPort'


class ToscaExtNetworkPort(ToscaNetworkPort):

    toscatype = 'tosca.nodes.network.Port'

    def get_hot_attribute(self, attribute, args):
        if attribute == 'ip_address':
            attr = {}
            attr['get_attr'] = [self.name, 'fixed_ips', '0', 'ip_address']
            return attr
        return super(ToscaExtNetworkPort, self).get_hot_attribute(attribute, args)
