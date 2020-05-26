from ignition.service.framework import Capability, interface, Service
from toscaparser.tosca_template import ToscaTemplate
from translator.hot.tosca_translator import TOSCATranslator
from osvimdriver.tosca.discover import ToscaTopologySearchEngine, NotDiscoveredError
import osvimdriver.tosca.definitions as tosca_definitions
import toscaparser.common.exception as toscaparser_exceptions
import yaml
import os

class ToscaValidationError(Exception):
    pass


class ToscaParserCapability(Capability):

    @interface
    def parse_tosca_str(self, tosca_str, inputs):
        pass


class ToscaParserService(Service, ToscaParserCapability):

    def parse_tosca_str(self, tosca_template_str, inputs=None, template_path=None):
        tosca_template = self.__load_yaml(tosca_template_str)
        if template_path is not None:
            self.__convert_relative_imports(tosca_template, template_path)
        self.include_extensions(tosca_template)
        try:
            return ToscaTemplate(None, inputs, False, tosca_template)
        except toscaparser_exceptions.ValidationError as e:
            raise ToscaValidationError(str(e)) from e

    def __load_yaml(self, template_str):
        return yaml.safe_load(template_str)

    def __convert_relative_imports(self, tosca_template_tpl, template_path):
        if 'imports' in tosca_template_tpl:
            if type(tosca_template_tpl['imports']) == list:
                original_imports = tosca_template_tpl['imports'].copy()
                new_imports = []
                for imp in original_imports:
                    if type(imp) == str and imp.startswith('./'):
                        template_dir = os.path.dirname(template_path)
                        abs_path_to_file = os.path.abspath(os.path.join(template_dir, imp[2:]))
                        new_imports.append(abs_path_to_file)
                    else:
                        new_imports.append(imp)
                tosca_template_tpl['imports'] = new_imports
                    
    def include_extensions(self, tosca_template_tpl):
        #with open(tosca_definitions.TYPE_EXTENSIONS_FILE) as extensions_file:
        #    extensions = yaml.safe_load(extensions_file.read())
        self.__add_extensions(tosca_definitions.TYPE_EXTENSIONS_FILE, tosca_template_tpl)
        if 'imports' in tosca_template_tpl:
            if type(tosca_template_tpl['imports']) == list and 'etsi_nfv_sol001' in tosca_template_tpl['imports']:
                self.__add_sol001_extensions(tosca_template_tpl)
                tosca_template_tpl['imports'].remove('etsi_nfv_sol001')

    def __add_sol001_extensions(self, tosca_template_tpl):
        self.__add_extensions(tosca_definitions.ETSI_COMMON_TYPES_FILE, tosca_template_tpl)
        self.__add_extensions(tosca_definitions.ETSI_VNFD_TYPES_FILE, tosca_template_tpl)
        self.__add_extensions(tosca_definitions.NFV_EXTENSIONS_FILE, tosca_template_tpl)
        
    def __add_extensions(self, ext_file, tosca_template_tpl):
        if 'imports' not in tosca_template_tpl:
            tosca_template_tpl['imports'] = []
        elif not isinstance(tosca_template_tpl['imports'], list):
            raise ToscaValidationError(f'imports must be a list but was {type(tosca_template_tpl["imports"])}')
        tosca_template_tpl['imports'].append(ext_file)

class ToscaHeatTranslatorCapability(Capability):

    @interface
    def generate_heat_template(self, tosca_template_str):
        pass


class ToscaHeatTranslatorService(Service, ToscaHeatTranslatorCapability):

    def __init__(self, **kwargs):
        if 'tosca_parser_service' not in kwargs:
            raise ValueError('No tosca_parser_service instance provided')
        self.tosca_parser_service = kwargs.get('tosca_parser_service')

    def generate_heat_template(self, tosca_template_str, template_path=None):
        if tosca_template_str is None:
            raise ValueError('Must provide tosca_template_str parameter')
        tosca = self.tosca_parser_service.parse_tosca_str(tosca_template_str, template_path=template_path)
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
