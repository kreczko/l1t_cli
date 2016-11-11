"""
    dqm gui start:
        starts the offline DQM GUI on port 8060
        
    Usage:
        dqm gui start

"""
import logging
import os
import hepshell
from hepshell.interpreter import time_function

LOG = logging.getLogger(__name__)

from l1t_cli.commands.dqm.gui.setup import DQM_GUI_PATH


class Command(hepshell.Command):

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)
        

    @time_function('dqm gui start', LOG)
    def run(self, args, variables):
        self.__prepare(args, variables)

        commands = [
            'cd {DQM_GUI_PATH}',
            'source current/apps/dqmgui/128/etc/profile.d/env.sh',
            '$PWD/current/config/dqmgui/manage -f dev start "I did read documentation"'
        ]

        all_in_one = ' && '.join(commands)
        all_in_one = all_in_one.format(DQM_GUI_PATH = DQM_GUI_PATH)
        
        from hepshell.interpreter import call
        code, _, stderr = call(all_in_one, logger=LOG, shell = True)
        if not code == 0:
            msg = 'Could not start DQM GUI: {0}'.format(stderr)
            LOG.error(msg)
            return False
        self.__text = 'DQM GUI now available at http://localhost:8060/dqm/dev'
        
        return True

    def __can_run(self):
        # if DQMOffline exists
        return True
