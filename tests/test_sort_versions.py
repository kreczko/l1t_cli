from l1t_cli.commands.get.latest.integration.tag import Command

import unittest


class Test(unittest.TestCase):

    def test_default_naming(self):
        versions = ['7.0', '84.3', '84.2']
        self.__verify(versions, '84.3')

    def test_with_extra_number(self):
        versions = ['3', '54.3.2', '54.3.5']
        self.__verify(versions, '54.3.5')
        
    def __verify(self, versions, latest_version):
        c = Command()
        result = c.get_latest_version(versions)
        self.assertEqual(result, latest_version)

if __name__ == "__main__":
    unittest.main()
