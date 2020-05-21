from translator.hot.tosca.etsi_nfv.tosca_nfv_vdu_compute import ToscaNfvVduCompute

TARGET_CLASS_NAME = 'OSNfvVduCompute'

CUSTOM_PROPS = ['admin_pass', 'availability_zone', 'config_drive', 'diskConfig', 'flavor', 'flavor_update_policy', 'image', 'image_update_policy', \
                    'key_name', 'metadata', 'name', 'reservation_id', 'scheduler_hints', 'security_groups', 'software_config_transport', \
                        'user_data', 'user_data_format', 'user_data_update_policy']

class OSNfvVduCompute(ToscaNfvVduCompute):
    """Translate TOSCA node type tosca.nodes.nfv.Vdu.Compute.NovaServer, an extension to tosca.nodes.nfv.Vdu.Compute"""

    toscatype = 'tosca.nodes.nfv.Vdu.Compute.NovaServer'

    def __init__(self, nodetemplate, csar_dir=None):
        super(OSNfvVduCompute, self).__init__(nodetemplate, csar_dir=csar_dir)

    def __is_custom_prop(self, prop_name):
        return prop_name in CUSTOM_PROPS

    def handle_properties(self):
        super().handle_properties()
        tosca_props = self.get_tosca_props()
        self.properties = {}
        user_data_params = None
        user_data = None
        for key, value in tosca_props.items():
            if self.__is_custom_prop(key):
                self.properties[key] = value
            if key == 'user_data_params':
                user_data_params = value
            elif key == 'user_data':
                user_data = value
        if user_data_params != None:
            new_user_data = {
                'str_replace': {
                    'params': user_data_params,
                    'template': user_data
                }
            }
            self.properties['user_data'] = new_user_data

    def get_hot_attribute(self, attribute, args):
        if attribute in CUSTOM_PROPS:
            attr = {}
            attr['get_attr'] = [self.name, attribute]
            return attr
        return super().get_hot_attribute(attribute, args)

    def handle_expansion(self):
        hot_resources = super(OSNfvVduCompute, self).handle_expansion()
        # Remove any empty flavours (where we haven't used the virtual_compute but the flavour attribute instead)
        if hot_resources != None and len(hot_resources) > 0:
            new_hot_resources = []
            for resource in hot_resources:
                if resource.type == 'OS::Nova::Flavor' and len(resource.properties) == 0:
                    pass
                else:
                    new_hot_resources.append(resource)
            hot_resources = new_hot_resources
        return hot_resources
