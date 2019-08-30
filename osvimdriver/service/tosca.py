from ignition.service.framework import Capability, interface, Service
from toscaparser.tosca_template import ToscaTemplate
from translator.hot.tosca_translator import TOSCATranslator
from osvimdriver.tosca.discover import ToscaTopologySearchEngine, NotDiscoveredError
import osvimdriver.tosca.definitions as tosca_definitions
import toscaparser.common.exception as toscaparser_exceptions
import yaml


class ToscaValidationError(Exception):
    pass


class ToscaParserCapability(Capability):

    @interface
    def parse_tosca_str(self, tosca_str, inputs):
        pass


class ToscaParserService(Service, ToscaParserCapability):

    def parse_tosca_str(self, tosca_template_str, inputs=None):
        tosca_template = yaml.safe_load(tosca_template_str)
        self.include_extensions(tosca_template)
        try:
            return ToscaTemplate(None, inputs, False, tosca_template)
        except toscaparser_exceptions.ValidationError as e:
            raise ToscaValidationError(str(e)) from e

    def include_extensions(self, tosca_template_tpl):
        with open(tosca_definitions.TYPE_EXTENSIONS_FILE) as extensions_file:
            extensions = yaml.safe_load(extensions_file.read())
        if 'node_types' in extensions:
            if 'node_types' not in tosca_template_tpl:
                tosca_template_tpl['node_types'] = {}
            for node_type_key, node_type_def in extensions['node_types'].items():
                if node_type_key not in tosca_template_tpl['node_types']:
                    tosca_template_tpl['node_types'][node_type_key] = node_type_def

    # Preferred way of adding extensions but the ToscaParser leaves the imported file open, which leads to python warnings for unclosed files
    # def __not_used_include_extensions(self, tosca_template):
    #    if 'imports' in tosca_template:
    #        imports = tosca_template['imports']
    #    else:
    #        imports = []
    #    imports.append({
    #        'type_extensions': {
    #            'file': tosca_definitions.TYPE_EXTENSIONS_FILE
    #        }
    #    })
    #    tosca_template['imports'] = imports


class ToscaHeatTranslatorCapability(Capability):

    @interface
    def generate_heat_template(self, tosca_template_str):
        pass


class ToscaHeatTranslatorService(Service, ToscaHeatTranslatorCapability):

    def __init__(self, **kwargs):
        if 'tosca_parser_service' not in kwargs:
            raise ValueError('No tosca_parser_service instance provided')
        self.tosca_parser_service = kwargs.get('tosca_parser_service')

    def generate_heat_template(self, tosca_template_str):
        if tosca_template_str is None:
            raise ValueError('Must provide tosca_template_str parameter')
        tosca = self.tosca_parser_service.parse_tosca_str(tosca_template_str)
        heat_translator = TOSCATranslator(tosca, {})
        # heat translator returns translated heat in a dict
        translation_dict_key = 'main_hot'
        heat_translations = heat_translator.translate_to_yaml_files_dict(translation_dict_key)
        heat_result = heat_translations[translation_dict_key]
        return heat_result


class ToscaTopologyDiscoveryCapability(Capability):

    @interface
    def discover(self, tosca_template_str, inputs, openstack_location):
        pass


class ToscaTopologyDiscoveryService(Service, ToscaTopologyDiscoveryCapability):

    def __init__(self, **kwargs):
        if 'tosca_parser_service' not in kwargs:
            raise ValueError('No tosca_parser_service instance provided')
        self.tosca_parser_service = kwargs.get('tosca_parser_service')

    def discover(self, tosca_template_str, openstack_location, inputs=None):
        if tosca_template_str is None:
            raise ValueError('Must provide tosca_template_str parameter')
        if openstack_location is None:
            raise ValueError('Must provide openstack_location parameter')
        tosca = self.tosca_parser_service.parse_tosca_str(tosca_template_str, inputs)
        return ToscaTopologySearchEngine(tosca, openstack_location).discover()
