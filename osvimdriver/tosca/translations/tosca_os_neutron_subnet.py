from osvimdriver.tosca.translations.os_hot_resource import OSHotResource

TARGET_CLASS_NAME = 'OSNeutronSubnet'
HOT_TYPE = 'OS::Neutron::Subnet'

LINKED_NETWORK_REL = 'tosca.relationships.network.LinksTo'

class OSNeutronSubnet(OSHotResource):
    '''Translate TOSCA node type tosca.nodes.network.NeutronSubnet'''

    toscatype = 'tosca.nodes.network.NeutronSubnet'

    def __init__(self, nodetemplate, csar_dir=None):
        super(OSNeutronSubnet, self).__init__(HOT_TYPE, nodetemplate, csar_dir=csar_dir)
    
    def handle_properties(self):
        super(OSNeutronSubnet, self).handle_properties()
        for rel, node in self.nodetemplate.relationships.items():
            # Check for attach relation. If found add a property for the attached network
            if rel.is_derived_from(LINKED_NETWORK_REL):
                attached_network_node = node
                network_resource = None
                for hot_resource in self.depends_on_nodes:
                    if attached_network_node.name == hot_resource.name:
                        network_resource = hot_resource
                        self.depends_on.remove(hot_resource)
                        break
                self.properties['network'] = '{ get_resource: %s }' % (attached_network_node.name)

