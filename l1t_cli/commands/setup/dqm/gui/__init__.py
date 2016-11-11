"""
    setup dqm gui:
        Sets up the DQM GUI. It will be available at port localhost:8060/dqm/dev

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


class Command(hepshell.Command):

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)

    @time_function('setup dqm gui', LOG)
    def run(self, args, variables):
        self.__prepare(args, variables)
            
        return True
