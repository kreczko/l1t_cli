from l1t_cli.commands.get.latest.integration.tag import Command

import unittest


class Test(unittest.TestCase):

    def test_default_naming(self):
        tags = ['l1t-o2o-integration-v7.0', 'l1t-integration-v84.3']
        versions = ['7.0', '84.3']
        self.__verify(tags, versions)

    def test_with_cmssw_version(self):
        tags = ['l1t-integration-v58.1-CMSSW_8_0_8',
                'l1t-integration-v54.0-CMSSW_8_0_8']
        versions = ['58.1', '54.0']
        self.__verify(tags, versions)

    def test_with_extra_number(self):
        tags = ['l1t-integration-v54.3.2']
        versions = ['54.3.2']
        self.__verify(tags, versions)
        
    def __verify(self, tags, versions):
        c = Command()
        for tag, version in zip(tags, versions):
            v = c.get_version(tag)
            self.assertEqual(v, version)

if __name__ == "__main__":
    unittest.main()
