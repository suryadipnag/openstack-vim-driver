from translator.hot.tosca.tosca_floating import ToscaFloatingIP

TARGET_CLASS_NAME = 'ToscaExtFloatingIp'
LINKED_NETWORK_REL = 'tosca.relationships.network.LinksTo'

class ToscaExtFloatingIp(ToscaFloatingIP):

    toscatype = 'tosca.nodes.network.FloatingIP'

    def handle_properties(self):
        super(ToscaExtFloatingIp, self).handle_properties()
        for rel, node in self.nodetemplate.relationships.items():
            # Check for attach relation. If found add a property for the attached network
            if rel.is_derived_from(LINKED_NETWORK_REL):
                attached_node = node
                if attached_node.type == 'tosca.nodes.network.Network' or attached_node.type == 'tosca.nodes.network.NeutronNetwork':
                    network_resource = None
                    for hot_resource in self.depends_on_nodes:
                        if attached_node.name == hot_resource.name:
                            network_resource = hot_resource
                            if hot_resource in self.depends_on:
                                self.depends_on.remove(hot_resource)
                            break
                    self.properties['floating_network'] = '{ get_resource: %s }' % (attached_node.name)

    def get_hot_attribute(self, attribute, args):
        if attribute == 'floating_ip_address':
            attr = {}
            attr['get_attr'] = [self.name, 'floating_ip_address']
            return attr
        return super(ToscaExtFloatingIp, self).get_hot_attribute(attribute, args)
