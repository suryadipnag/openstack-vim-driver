import yaml


class HeatInputUtil:

    def filter_used_properties(self, heat_template_str, original_properties):
        heat_tpl = yaml.safe_load(heat_template_str)
        used_properties = {}
        if 'parameters' in heat_tpl:
            for k, v in heat_tpl['parameters'].items():
                if k in original_properties:
                    used_properties[k] = original_properties[k]
        return used_properties
