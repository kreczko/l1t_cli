"""
    run within cmssw:
        Runs a command within a CMS Software (CMSSW) setup.

        Usage:
            run within cmssw "command" cmssw_path=<>

        Parameters:
            command: the command to run
            
            cmssw_path: path to the CMSSW setup
"""
import logging
import os

from l1t_cli.commands import Command as C
from l1t_cli.setup import CMSSW_SRC

LOG = logging.getLogger(__name__)


class Command(C):

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)

    def run(self, args, variables):
        self.__prepare(args, variables)
        
        self.__command == self.__variables['command']
        self.__text = 'NOT IMPLEMENTED YET'

        return True


def run_within_cmssw(command, cmssw_src=CMSSW_SRC, logger=LOG):
    commands = [
        'cd {CMSSW_SRC}',
        'source /cvmfs/cms.cern.ch/cmsset_default.sh',
        'eval `/cvmfs/cms.cern.ch/common/scram runtime -sh`',
    ]

    all_in_one = ' && '.join(commands)
    all_in_one = all_in_one + ' && ' + command + ' \n'
    all_in_one = all_in_one.format(CMSSW_SRC=cmssw_src)
    from hepshell.interpreter import call
    return_code, stdout, stderr = call(all_in_one, logger=logger, shell=True)

    return return_code, stdout, stderr
