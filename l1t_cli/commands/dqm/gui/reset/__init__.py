"""
    dqm gui reset:
        Removes the current GUI installation and creates a new one
        
    Usage:
        dqm gui reset

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
        

    @time_function('dqm gui reset', LOG)
    def run(self, args, variables):
        self.__prepare(args, variables)
        
        if not os.path.exists(DQM_GUI_PATH):
            LOG.error('Cannot run since DQM PATH does not exist')
            return False
        
        from l1t_cli.commands.dqm.gui.remove import Command as RemoveCommand
        rm = RemoveCommand()
        rm.run([], {})
        
        from l1t_cli.commands.dqm.gui.setup import Command as SetupCommand
        setup = SetupCommand()
        setup.run([], {})
        
        from l1t_cli.commands.dqm.gui.start import Command as StartCommand
        SetupCommand().run([], {})
        
        return True
