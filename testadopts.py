import uuid
import tempfile
import shutil
import os
import time
from ignition.service.resourcedriver import InfrastructureNotFoundError, InvalidDriverFilesError, InvalidRequestError
from ignition.model.references import FindReferenceResponse, FindReferenceResult
from ignition.model.associated_topology import AssociatedTopology
from ignition.model.lifecycle import LifecycleExecution, LifecycleExecuteResponse
from ignition.utils.file import DirectoryTree
from osvimdriver.service.resourcedriver import ResourceDriverHandler, StackNameCreator, PropertiesMerger, AdditionalResourceDriverProperties, AdoptProperties
from osvimdriver.service.tosca import ToscaValidationError
from osvimdriver.tosca.discover import DiscoveryResult, NotDiscoveredError
from osvimdriver.openstack.heat.driver import StackNotFoundError
from osvimdriver.openstack.environment import OpenstackDeploymentLocationTranslator
from ignition.utils.propvaluemap import PropValueMap

class OSConnector:
    resource_driver_config = AdditionalResourceDriverProperties()
    adopt_properties = AdoptProperties()
    def setupResourceDriver(self):
        driver = ResourceDriverHandler(OpenstackDeploymentLocationTranslator(), 
            resource_driver_config=self.resource_driver_config, heat_translator_service=None, tosca_discovery_service=None,
            adopt_config=self.adopt_properties)
        return driver

class ConnectionRunner:

    def __create_mock_driver_files(self):
        heat_driver_files_path = tempfile.mkdtemp()
        self.heat_template = 'heat_template'
        with open(os.path.join(heat_driver_files_path, 'heat.yaml'), 'w') as f:
            f.write(self.heat_template)
        tosca_driver_files_path = tempfile.mkdtemp()
        self.tosca_template = 'tosca_template'
        self.tosca_template_path = os.path.join(tosca_driver_files_path, 'tosca.yaml')
        with open(self.tosca_template_path, 'w') as f:
            f.write(self.tosca_template)
        self.discover_template = 'discover_template'
        with open(os.path.join(tosca_driver_files_path, 'discover.yaml'), 'w') as f:
            f.write(self.discover_template)
        self.heat_driver_files = DirectoryTree(heat_driver_files_path)
        self.tosca_driver_files = DirectoryTree(tosca_driver_files_path)    


    def __resource_properties(self):
        props = {}
        props['propA'] = {'type': 'string', 'value': 'valueA'}
        props['propB'] = {'type': 'string', 'value': 'valueB'}
        return PropValueMap(props)

    def __system_properties(self):
        props = {}
        props['resourceId'] = '123'
        props['resourceName'] = 'TestResource'
        return PropValueMap(props)        

    def __created_associated_topology(self, adopt=False):
        associated_topology = AssociatedTopology()
        if adopt==True:
            stack_id = 'f96b3c43-66a0-4b4f-a822-38cd313afff5'
            associated_topology.add_entry(stack_id, stack_id, 'Openstack')
        else:
            associated_topology.add_entry('InfrastructureStack', '1', 'Openstack')    
        return associated_topology


    def __deployment_location(self):
        return {
            "name": "openstack-yeast",
            "properties": {
                "os_auth_project_name": "bluesquad",
                "os_auth_project_domain_name": "default",
                "os_auth_username": "admin",
                "os_auth_password": "password", 
                "os_auth_user_domain_name": "Default",
                "os_auth_api": "identity/v3",
                "os_api_url": "http://9.46.89.226",
                "os_auth_project_id": "701600a059af40e1865a3c494288712a"},             
            "type": "Openstack"
        }             

    def doIt(self):
        connectTest = OSConnector()
        driver = connectTest.setupResourceDriver()
        print("Set Up parameters");
        self.__create_mock_driver_files()       
        self.resource_properties = self.__resource_properties()
        self.system_properties = self.__system_properties()        
        self.created_adopted_topology = self.__created_associated_topology(True)
        self.deployment_location = self.__deployment_location()

        print("Call execute_lifecycle to Adopt:" +str(self.created_adopted_topology));

        executionRequestResponse = driver.execute_lifecycle("Adopt", self.heat_driver_files, self.system_properties, self.resource_properties, {}, self.created_adopted_topology, self.deployment_location)
       
        print("Call get_lifecycle_execution... for request: "+str(executionRequestResponse.request_id))
        
        for x in range(0, 6): 
            executionResponse = driver.get_lifecycle_execution(executionRequestResponse.request_id, self.deployment_location)
            if executionResponse.status == 'IN_PROGRESS':
                executionResponse = driver.get_lifecycle_execution(executionRequestResponse.request_id, self.deployment_location)
                print("In Progress, wait 5s... "+str(x))
                time.sleep(5)
            else:
                break

        print("response: "+executionResponse.status)
        print("response outputs: "+str(executionResponse.outputs))
        print("request ID: "+str(executionResponse.request_id))
        print("failure_details: "+str(executionResponse.failure_details))


runner = ConnectionRunner()
runner.doIt()
