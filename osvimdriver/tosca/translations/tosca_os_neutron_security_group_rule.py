from osvimdriver.tosca.translations.os_hot_resource import OSHotResource

TARGET_CLASS_NAME = 'OSSecurityGroupRule'
HOT_TYPE = 'OS::Neutron::SecurityGroupRule'

class OSSecurityGroupRule(OSHotResource):
    '''Translate TOSCA node type tosca.nodes.network.NeutronSecurityGroupRule'''

    toscatype = 'tosca.nodes.network.NeutronSecurityGroupRule'

    def __init__(self, nodetemplate, csar_dir=None):
        super(OSSecurityGroupRule, self).__init__(HOT_TYPE, nodetemplate, csar_dir=csar_dir)
    
    
