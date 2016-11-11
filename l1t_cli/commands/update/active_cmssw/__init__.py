"""
    update active_cmssw:
        Changed the workspace/active_cmssw link to a new project area

        Usage:
            update active_cmssw <new project area>
"""
import logging
import os
import getpass

import hepshell

from hepshell.interpreter import time_function
from l1t_cli.setup import WORKSPACE
LOG = logging.getLogger(__name__)


class Command(hepshell.Command):

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)

    @time_function('update active_cmssw', LOG)
    def run(self, args, variables):
        self.__prepare(args, variables)
        
        if not args:
            LOG.error('No new project area defined')
            return False
        
        path = os.path.abspath(args[0])
        symlink = os.path.join(WORKSPACE, 'active_cmssw') # change to active_cmssw?
        
        destination = os.path.relpath(path, WORKSPACE)
         
        from l1t_cli.common import update_symlink
        update_symlink(symlink, destination)
        
        return True
