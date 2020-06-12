from osvimdriver.tosca.translations.os_hot_resource import OSHotResource

TARGET_CLASS_NAME = 'OSSecurityGroup'
HOT_TYPE = 'OS::Neutron::SecurityGroup'

class OSSecurityGroup(OSHotResource):
    '''Translate TOSCA node type tosca.nodes.network.NeutronSecurityGroup'''

    toscatype = 'tosca.nodes.network.NeutronSecurityGroup'

    def __init__(self, nodetemplate, csar_dir=None):
        super(OSSecurityGroup, self).__init__(HOT_TYPE, nodetemplate, csar_dir=csar_dir)
    
    
