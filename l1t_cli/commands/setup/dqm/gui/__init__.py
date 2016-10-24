"""
    setup dqm gui:
        Sets up the DQM GUI. It will be available at port localhost:8060/dqm/dev
        From https://twiki.cern.ch/twiki/bin/view/CMS/DQMGuiForUsers

        Usage:
            setup dqm gui
"""
import logging
import os
import string
import hepshell

from hepshell.interpreter import time_function
from l1t_cli.setup import WORKSPACE
from l1t_cli.setup import INTEGRATION_TAG

LOG = logging.getLogger(__name__)

DQM_GIT = 'https://github.com/dmwm/deployment.git'
DQM_PATH = os.path.join(WORKSPACE, 'dqm')
DQM_GUI_PATH = os.path.join(DQM_PATH, 'gui')
# latest tag from https://github.com/dmwm/deployment/releases
DQM_TAG = 'HG1610a'
SCRAM_ARCH = 'slc6_amd64_gcc493'


class Command(hepshell.Command):

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)

    @time_function('setup dqm gui', LOG)
    def run(self, args, variables):
        self.__prepare(args, variables)
        if not self.__can_run():
            return False

        os.makedirs(DQM_GUI_PATH)

        from hepshell.interpreter import call
        git_command = 'git clone {DQM_GIT} {DQM_GUI_PATH}/deployment'.format(
            DQM_GIT=DQM_GIT, DQM_GUI_PATH=DQM_GUI_PATH
        )
        code, _, err = call(git_command, logger=LOG, shell=True)
        if not code == 0:
            self.__text = 'Something went wrong:\n'
            self.__text += err

        deploy_command = ' '.join([
            '{DQM_GUI_PATH}/deployment/Deploy',
            '-A {SCRAM_ARCH}',
            '-r "comp=comp"',
            '-R comp@{DQM_TAG}',
            '-t MYDEV',
            '-s "prep sw post"',
            DQM_GUI_PATH,
            'dqmgui/bare',
        ]
        )
        deploy_command = deploy_command.format(
            DQM_GUI_PATH=DQM_GUI_PATH, SCRAM_ARCH=SCRAM_ARCH, DQM_TAG=DQM_TAG
        )
        code, _, err = call(deploy_command, logger=LOG, shell=True)
        if not code == 0:
            self.__text = 'Something went wrong:\n'
            self.__text += err

        self.__text = 'You can now run "l1t run dqm gui"'

        return True

    def __can_run(self):
        return not os.path.exists(DQM_GUI_PATH)
