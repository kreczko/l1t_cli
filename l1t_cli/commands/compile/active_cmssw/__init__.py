"""
    compile active_cmssw:
        Compiles the CMSSW version which is linked under workspace/current
        
    Usage:
        compile [ncpu=1]
        
    Parameters:
        npcu: number of CPUs to be used for compilation. Default: 1
"""
import logging
import hepshell
import os
from hepshell.interpreter import time_function

LOG = logging.getLogger(__name__)
from l1t_cli.setup import ACTIVE_CMSSW
CMSSW_SRC = os.path.join(ACTIVE_CMSSW, 'src')


class Command(hepshell.Command):

    DEFAULTS = {
        'ncpu': 1,
    }

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)

    @time_function('compile', LOG)
    def run(self, args, variables):
        if not self.__can_run():
            return False
        self.__prepare(args, variables)
        n_jobs = int(self.__variables['ncpu'])
        commands = [
            'cd {CMSSW_SRC}',
            'source /cvmfs/cms.cern.ch/cmsset_default.sh',
            'eval `/cvmfs/cms.cern.ch/common/scram runtime -sh`',
            'scram b -j{n_jobs}'
        ]

        all_in_one = ' && '.join(commands)
        all_in_one = all_in_one.format(CMSSW_SRC=CMSSW_SRC, n_jobs=n_jobs)

        from hepshell.interpreter import call
        call(all_in_one, logger=LOG, shell=True)

        return True

    def __can_run(self):
        if not os.path.exists(CMSSW_SRC):
            LOG.error('CMSSW is not set up: {0}'.format(CMSSW_SRC))
            return False

        return True
