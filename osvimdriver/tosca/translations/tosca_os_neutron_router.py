from osvimdriver.tosca.translations.os_hot_resource import OSHotResource

TARGET_CLASS_NAME = 'OSNeutronRouter'
HOT_TYPE = 'OS::Neutron::Router'

class OSNeutronRouter(OSHotResource):
    '''Translate TOSCA node type tosca.nodes.network.NeutronRouter'''

    toscatype = 'tosca.nodes.network.NeutronRouter'

    def __init__(self, nodetemplate, csar_dir=None):
        super(OSNeutronRouter, self).__init__(HOT_TYPE, nodetemplate, csar_dir=csar_dir)
    
    
