"""
    dqm offline setup:
        Sets up CMSSW and the latest code to preduce OfflineDQM plots

        Usage:
            dqm offline setup
"""
import logging
import os
import string
import hepshell

from hepshell.interpreter import time_function
from l1t_cli.setup import WORKSPACE, INTEGRATION_TAG

LOG = logging.getLogger(__name__)

RECIPE = {
    'cmssw_version': 'CMSSW_8_1_0_pre15',
    'scram_arch': 'slc6_amd64_gcc530',
    'l1t_version': INTEGRATION_TAG,
    'alias': 'DQMOffline',
}


class Command(hepshell.Command):

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)

    @time_function('dqm offline setup', LOG)
    def run(self, args, variables):
        self.__prepare(args, variables)
        self.__version = RECIPE['cmssw_version']

        if not os.path.exists(WORKSPACE):
            os.mkdir(WORKSPACE)

        from l1t_cli.commands.setup.cmssw import Command as CMSSetup
        params = {
            'version': RECIPE['cmssw_version'],
            'scram_arch': RECIPE['scram_arch'],
            'alias': RECIPE['alias'],
            'parent_folder': WORKSPACE,
            'init-git': True,
        }
        cmssw = CMSSetup()
        cmssw.run([], params)

        commands = [
            #'git remote add cms-l1t-offline https://github.com/cms-l1t-offline/cmssw.git',
            #'git fetch cms-l1t-offline',
            #'git cms-merge-topic --unsafe cms-l1t-offline:{0}'.format(RECIPE['l1t_version']),
            'git cms-addpkg DQMServices/Examples',
            'git cms-addpkg DQMServices/Components',
            'git cms-addpkg DQMOffline/L1Trigger',
            'git cms-merge-topic kreczko:offlineDQM-l1tEGamma'
            'scram b jobs=2',
        ]
        from l1t_cli.commands.run.within.cmssw import Command as RunCMSSW
        cmssw = RunCMSSW()
        run_cmssw = cmssw.run
        parameters = {'cmssw_path': os.path.join(WORKSPACE, RECIPE['alias'])}

        for command in commands:
            success = run_cmssw(args=[command], variables=parameters)
            if not success:  # stop at first error
                return False

        # now activate the working area:
        from l1t_cli.commands.update.active_cmssw import Command as UpdateCMSSW
        c = UpdateCMSSW()
        new_cmssw = os.path.join(WORKSPACE, RECIPE['alias'])
        c.run([new_cmssw], {})

        return True
