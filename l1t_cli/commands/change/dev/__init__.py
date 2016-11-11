"""
    change dev:
        Changed the DEV link to a new project area

        Usage:
            change dev <new project area>
"""
import logging
import os
import getpass

from hepshell.interpreter import time_function
import hepshell
LOG = logging.getLogger(__name__)


class Command(hepshell.Command):

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)

    @time_function('change dev', LOG)
    def run(self, args, variables):
        self.__prepare(args, variables)
        
        if not args:
            LOG.error('No new project area defined')
            return False
        
        path = os.path.abspath(args[0])
        source = 'DEV'
        destination = os.path.relpath(path, hepshell.HEP_PROJECT_ROOT)
         
        from l1t_cli.common import update_symlink
        update_symlink(source, destination)
        
        return True
