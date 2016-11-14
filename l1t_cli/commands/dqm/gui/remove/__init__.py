"""
    dqm gui remove:
        Removes the current GUI installation
        
    Usage:
        dqm gui remove

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
        

    @time_function('dqm gui remove', LOG)
    def run(self, args, variables):
        self.__prepare(args, variables)
        
        if not os.path.exists(DQM_GUI_PATH):
            LOG.error('Cannot run since DQM PATH does not exist')
            return False
        
        from l1t_cli.commands.dqm.gui import is_dqm_gui_running
        if is_dqm_gui_running():
            # stop it first
            from l1t_cli.commands.dqm.gui.stop import Command as StopCommand
            stop = StopCommand()
            stop.run([], {})
        
        import shutil
        shutil.rmtree(DQM_GUI_PATH)
        
        return True
