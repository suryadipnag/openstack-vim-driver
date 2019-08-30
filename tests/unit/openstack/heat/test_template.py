import unittest
from osvimdriver.openstack.heat.template import HeatInputUtil


class TestHeatInputUtil(unittest.TestCase):

    def test_filter_used_properties(self):
        util = HeatInputUtil()
        heat_yml = '''
        parameters: 
          propA: 
            type: string
          propB:
            type: string
        '''
        orig_props = {'propA': 'testA', 'propB': 'testB', 'propC': 'testC'}
        new_props = util.filter_used_properties(heat_yml, orig_props)
        self.assertEqual(new_props, {'propA': 'testA', 'propB': 'testB'})
