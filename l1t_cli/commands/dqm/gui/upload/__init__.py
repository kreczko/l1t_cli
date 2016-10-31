"""
    dqm gui upload:
        Uploads a file to the offline DQM GUI on port 8060
        
    Usage:
        dqm gui upload <file>

"""
import logging
import os
import hepshell
from hepshell.interpreter import time_function

LOG = logging.getLogger(__name__)

from l1t_cli.commands.setup.dqm.gui import DQM_GUI_PATH


class Command(hepshell.Command):

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)
        

    @time_function('dqm gui upload', LOG)
    def run(self, args, variables):
        self.__prepare(args, variables)
        
        self.__file = os.path.abspath(self.__args[0])

        commands = [
            'cd {DQM_GUI_PATH}',
            'source current/apps/dqmgui/128/etc/profile.d/env.sh',
            'visDQMUpload http://localhost:8060/dqm/dev {file_name}'
        ]

        all_in_one = ' && '.join(commands)
        all_in_one = all_in_one.format(
            DQM_GUI_PATH = DQM_GUI_PATH,
            file_name = self.__file,
        )
        
        from hepshell.interpreter import call
        code, _, stderr = call(all_in_one, logger=LOG, shell = True)
        if not code == 0:
            msg = 'Could not upload to DQM GUI: {0}'.format(stderr)
            LOG.error(msg)
            return False
        self.__text = 'Uploaded {0} to DQM GUI'.format(self.__file)
        
        return True

    def __can_run(self):
        file_exists = os.path.exists(self.__file)
        
        dqm_is_running = self.__is_dqm_gui_running()
        return file_exists and dqm_is_running
    
    def __is_dqm_gui_running(self):
        pid_file = os.path.join(DQM_GUI_PATH, 'state/dqmgui/dev/pid')
        if not os.path.exists(pid_file):
            return False
        with open(pid_file) as f:
            pid = int(f.readLines())

        import psutil
        dqm_is_running = psutil.pid_exists(pid)
        return dqm_is_running
