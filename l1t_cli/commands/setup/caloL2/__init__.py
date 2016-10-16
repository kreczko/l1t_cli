"""
    setup caloL2: Sets up CMSSW and the latest code to preduce CaloL2 ntuples
        Usage:
            setup caloL2
"""
import logging
import os
import string
import hepshell

from hepshell.interpreter import time_function
from l1t_cli.setup import WORKSPACE

LOG = logging.getLogger(__name__)

RECIPE = {
    'cmssw_version': 'CMSSW_8_0_9',
    'scram_arch': 'slc6_amd64_gcc530',
    'l1t_version': 'l1t-integration-v77.0',
}


class Command(hepshell.Command):

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)

    @time_function('setup caloL2', LOG)
    def run(self, args, variables):
        self.__prepare(args, variables)
        self.__version = RECIPE['cmssw_version']

        if not os.path.exists(WORKSPACE):
            os.mkdir(WORKSPACE)

        if not self.__can_run():
            return False

        commands = [
            'git cms-init',
            'git remote add cms-l1t-offline https://github.com/cms-l1t-offline/cmssw.git',
            'git fetch cms-l1t-offline',
            'git cms-merge-topic --unsafe cms-l1t-offline:{0}'.format(RECIPE['l1t_version']),
            'scram b jobs=2',
        ]

        cmssw_env = [
            'cd {WORKSPACE}',
            'export SCRAM_ARCH={scram_arch}',
            'source /cvmfs/cms.cern.ch/cmsset_default.sh',
            '/cvmfs/cms.cern.ch/common/scram project CMSSW {cmssw_version}',
            'cd {cmssw_version}/src',
            'eval `/cvmfs/cms.cern.ch/common/scram runtime -sh`',
        ]

        cmsenv = ' && '.join(cmssw_env)
        cmsenv = cmsenv.format(
            WORKSPACE=WORKSPACE,
            scram_arch=RECIPE['scram_arch'],
            cmssw_version=RECIPE['cmssw_version'],
        )
        
        from hepshell.interpreter import call
        for command in commands:
            all_in_one = ' {0} && {1}'.format(cmsenv, command)
            call(all_in_one, logger=LOG, shell=True)
            
        return True

    def __can_run(self):
        if os.path.exists(WORKSPACE + '/' + self.__version):
            LOG.error('CMSSW is already set up: {0}'.format(
                WORKSPACE + '/' + self.__version))
            return False
        return True
