import logging
import ignition.boot.api as ignition
import osvimdriver.config as osvimdriverconfig
import pathlib
import os
from osvimdriver.service.infrastructure import InfrastructureDriver
from osvimdriver.openstack.environment import OpenstackDeploymentLocationTranslator
from osvimdriver.service.tosca import ToscaParserCapability, ToscaHeatTranslatorCapability, ToscaParserService, ToscaHeatTranslatorService, ToscaTopologyDiscoveryService, ToscaTopologyDiscoveryCapability
from osvimdriver.service.osadmin import OpenstackAdminApiConfigurator, OpenstackAdminServiceConfigurator, OpenstackAdminProperties

default_config_dir_path = str(pathlib.Path(osvimdriverconfig.__file__).parent.resolve())
default_config_path = os.path.join(default_config_dir_path, 'ovd_config.yml')


def create_app():
    logging.basicConfig(level=logging.DEBUG)

    app_builder = ignition.build_vim_driver('Openstack VIM Driver')
    app_builder.include_file_config_properties(default_config_path, required=True)
    app_builder.include_file_config_properties('./ovd_config.yml', required=False)
    # custom config file e.g. for K8s populated from Helm chart values
    app_builder.include_file_config_properties('/var/ovd/ovd_config.yml', required=False)
    app_builder.include_environment_config_properties('OVD_CONFIG', required=False)
    app_builder.add_service(ToscaParserService)
    app_builder.add_service(ToscaTopologyDiscoveryService, tosca_parser_service=ToscaParserCapability)
    app_builder.add_service(ToscaHeatTranslatorService, tosca_parser_service=ToscaParserCapability)
    app_builder.add_service(InfrastructureDriver, OpenstackDeploymentLocationTranslator(),
                            heat_translator_service=ToscaHeatTranslatorCapability, tosca_discovery_service=ToscaTopologyDiscoveryCapability)

    # Custom Property Group, Service and API
    app_builder.add_property_group(OpenstackAdminProperties())
    app_builder.add_api_configurator(OpenstackAdminApiConfigurator())
    app_builder.add_service_configurator(OpenstackAdminServiceConfigurator())

    return app_builder.configure()


def init_app():
    app = create_app()
    return app.run()
