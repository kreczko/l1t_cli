"""
    dqm offline run:
        Runs the L1 Trigger offline DQM sequences (just L1 Trigger offline!)
        
    Usage:
        dqm offline run

"""
import logging
import os
import hepshell
from hepshell.interpreter import time_function

LOG = logging.getLogger(__name__)

from l1t_cli.commands.dqm.offline.setup import RECIPE
from l1t_cli.setup import WORKSPACE


class Command(hepshell.Command):

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)
        base_path = os.path.join(
            WORKSPACE, RECIPE['alias'], 'src', 'DQMOffline/L1Trigger/test/'
        )
        self.__step1 = os.path.join(
            base_path, 'runDQMOffline_step1_L1TStage2CaloLayer2_cfg.py'
#             base_path, 'test_L1T_offline.py'
        )
        self.__step2 = os.path.join(
            base_path, 'runDQMOffline_step2_L1TStage2CaloLayer2_cfg.py'
        )
        self.__cmssw_path = os.path.join(WORKSPACE, RECIPE['alias'])

    @time_function('dqm offline run', LOG)
    def run(self, args, variables):
        self.__prepare(args, variables)

        commands = [
            'cmsRun {0}'.format(self.__step1),
            'cmsRun {0}'.format(self.__step2),
            # TODO: check if DQM GUI is running and upload result
        ]

        from l1t_cli.commands.run.within.cmssw import Command as CMSSW
        cmssw = CMSSW()

        results = []
        for command in commands:
            result = cmssw.run([command], {'cmssw_path': self.__cmssw_path})
            if not result:
                LOG.error('An error occurred')
                return False
            results.append(result)
            

        return all(results)

    def __can_run(self):
        # if DQMOffline exists
        return True
