"""
    run within cmssw:
        Runs a command within a CMS Software (CMSSW) setup.

        Usage:
            run within cmssw "command" cmssw_path=<>

        Parameters:
            command: the command to run
            
            cmssw_path: path to the CMSSW setup.
"""
import logging
import os
import hepshell

from l1t_cli.setup import CMSSW_BASE

LOG = logging.getLogger(__name__)


class Command(hepshell.Command):

    DEFAULTS = {
        'cmssw_path': CMSSW_BASE
    }

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)

    def run(self, args, variables):
        self.__prepare(args, variables)
        cmssw_path = self.__variables['cmssw_path']
        if not os.path.exists(cmssw_path):
            self.__text = "Could not find CMSSW area '{0}'".format(cmssw_path)
            return False
        self.__command = args[0]

        commands = [
            'cd {cmssw_path}/src',
            'source /cvmfs/cms.cern.ch/cmsset_default.sh',
            'eval `/cvmfs/cms.cern.ch/common/scram runtime -sh`',
        ]
        commands.append(self.__command)
        all_in_one = ' && '.join(commands)
        all_in_one = all_in_one.format(cmssw_path=cmssw_path)
        from hepshell.interpreter import call
        return_code, stdout, stderr = call(all_in_one, logger=LOG, shell=True)
        if return_code == 0:
            self.__text = stdout
            return True
        else:
            self.__text = 'An error occurred when executing\n'
            self.__text += '"{command}"\n'.format(command=self.__command)
            self.__text += 'within CMSSW ({cmssw_path}/src):\n'.format(
                cmssw_path=cmssw_path)
            self.__text += stderr
            return False

        return True
