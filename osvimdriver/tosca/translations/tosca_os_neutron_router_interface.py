from osvimdriver.tosca.translations.os_hot_resource import OSHotResource

TARGET_CLASS_NAME = 'OSNeutronRouterInterface'
HOT_TYPE = 'OS::Neutron::RouterInterface'

class OSNeutronRouterInterface(OSHotResource):
    '''Translate TOSCA node type tosca.nodes.network.NeutronRouterInterface'''

    toscatype = 'tosca.nodes.network.NeutronRouterInterface'

    def __init__(self, nodetemplate, csar_dir=None):
        super(OSNeutronRouterInterface, self).__init__(HOT_TYPE, nodetemplate, csar_dir=csar_dir)
    
    
