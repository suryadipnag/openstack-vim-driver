import unittest
from unittest.mock import MagicMock, patch
import os
import yaml
from osvimdriver.service.tosca import ToscaHeatTranslatorService, ToscaParserService, ToscaTopologyDiscoveryService, ToscaValidationError
from tests.unit.testutils.constants import TOSCA_TEMPLATES_PATH, TOSCA_HELLO_WORLD_FILE, HEAT_TEMPLATES_PATH, HEAT_HELLO_WORLD_FILE, TOSCA_DISCOVER_NETWORK_WITH_INPUTS_AND_OUTPUTS_FILE, TOSCA_MISSING_INPUT_FILE
from toscaparser.tosca_template import ToscaTemplate

tosca_templates_dir = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, TOSCA_TEMPLATES_PATH)
hello_world_tosca_file = os.path.join(tosca_templates_dir, TOSCA_HELLO_WORLD_FILE)
discover_network_with_inputs_and_outputs_tosca_file = os.path.join(tosca_templates_dir, TOSCA_DISCOVER_NETWORK_WITH_INPUTS_AND_OUTPUTS_FILE)
missing_input_tosca_file = os.path.join(tosca_templates_dir, TOSCA_MISSING_INPUT_FILE)


heat_templates_dir = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, HEAT_TEMPLATES_PATH)
hello_world_heat_file = os.path.join(heat_templates_dir, HEAT_HELLO_WORLD_FILE)


class TestToscaHeatTranslatorService(unittest.TestCase):

    def test_generate_heat_template(self):
        with open(hello_world_tosca_file, 'r') as tosca_reader:
            tosca_template = tosca_reader.read()
        mock_tosca_parser_service = MagicMock()
        mock_tosca_parser_service.parse_tosca_str.return_value = ToscaTemplate(None, None, False, yaml.safe_load(tosca_template))
        translator = ToscaHeatTranslatorService(tosca_parser_service=mock_tosca_parser_service)
        heat = translator.generate_heat_template(tosca_template)
        with open(hello_world_heat_file, 'r') as heat_reader:
            expected_heat = heat_reader.read()
        heat_tpl = yaml.safe_load(heat)
        expected_heat_tpl = yaml.safe_load(expected_heat)
        self.assertDictEqual(heat_tpl, expected_heat_tpl)

    def test_generate_heat_template_missing_tosca_template(self):
        mock_tosca_parser_service = MagicMock()
        translator = ToscaHeatTranslatorService(tosca_parser_service=mock_tosca_parser_service)
        with self.assertRaises(ValueError) as context:
            translator.generate_heat_template(None)
        self.assertEqual(str(context.exception), 'Must provide tosca_template_str parameter')


class TestToscaParserService(unittest.TestCase):

    @patch('osvimdriver.service.tosca.ToscaTemplate')
    def test_parse_tosca_str(self, mock_tosca_template_init):
        with open(hello_world_tosca_file, 'r') as tosca_reader:
            tosca_template = tosca_reader.read()
        parser = ToscaParserService()
        parse_result = parser.parse_tosca_str(tosca_template)
        expected_tosca = yaml.safe_load(tosca_template)
        parser.include_extensions(expected_tosca)
        mock_tosca_template_init.assert_called_once_with(None, None, False, expected_tosca)
        self.assertEqual(parse_result, mock_tosca_template_init.return_value)

    def test_parser_tosca_str_throws_validation_error(self):
        with open(missing_input_tosca_file, 'r') as tosca_reader:
            tosca_template = tosca_reader.read()
        parser = ToscaParserService()
        with self.assertRaises(ToscaValidationError) as e:
            parser.parse_tosca_str(tosca_template)


class TestToscaTopologyDiscoveryService(unittest.TestCase):

    def test_init_without_parser_service_fails(self):
        with self.assertRaises(ValueError) as context:
            ToscaTopologyDiscoveryService()
        self.assertEqual(str(context.exception), 'No tosca_parser_service instance provided')

    def test_discover_without_tosca_str_fails(self):
        mock_tosca_parser = MagicMock()
        discovery_service = ToscaTopologyDiscoveryService(tosca_parser_service=mock_tosca_parser)
        with self.assertRaises(ValueError) as context:
            discovery_service.discover(None, MagicMock())
        self.assertEqual(str(context.exception), 'Must provide tosca_template_str parameter')

    def test_discover_without_openstack_location_fails(self):
        with open(discover_network_with_inputs_and_outputs_tosca_file, 'r') as tosca_reader:
            tosca_template = tosca_reader.read()
        mock_tosca_parser = MagicMock()
        discovery_service = ToscaTopologyDiscoveryService(tosca_parser_service=mock_tosca_parser)
        with self.assertRaises(ValueError) as context:
            discovery_service.discover(tosca_template, None)
        self.assertEqual(str(context.exception), 'Must provide openstack_location parameter')

    @patch('osvimdriver.service.tosca.ToscaTopologySearchEngine')
    def test_discover(self, mock_search_engine_init):
        with open(discover_network_with_inputs_and_outputs_tosca_file, 'r') as tosca_reader:
            tosca_template = tosca_reader.read()
        mock_tosca_parser = MagicMock()
        mock_openstack_location = MagicMock()
        discovery_service = ToscaTopologyDiscoveryService(tosca_parser_service=mock_tosca_parser)
        discovery_service.discover(tosca_template, mock_openstack_location)
        mock_tosca_parser.parse_tosca_str.assert_called_once_with(tosca_template, None)
        mock_search_engine_init.assert_called_once_with(mock_tosca_parser.parse_tosca_str.return_value, mock_openstack_location)
        mock_search_engine_init.return_value.discover.assert_called_once()

    @patch('osvimdriver.service.tosca.ToscaTopologySearchEngine')
    def test_discover_with_inputs(self, mock_search_engine_init):
        with open(discover_network_with_inputs_and_outputs_tosca_file, 'r') as tosca_reader:
            tosca_template = tosca_reader.read()
        mock_tosca_parser = MagicMock()
        mock_openstack_location = MagicMock()
        discovery_service = ToscaTopologyDiscoveryService(tosca_parser_service=mock_tosca_parser)
        discovery_service.discover(tosca_template, mock_openstack_location, {'network_name': 'abc'})
        mock_tosca_parser.parse_tosca_str.assert_called_once_with(tosca_template, {'network_name': 'abc'})
        mock_search_engine_init.assert_called_once_with(mock_tosca_parser.parse_tosca_str.return_value, mock_openstack_location)
        mock_search_engine_init.return_value.discover.assert_called_once()
