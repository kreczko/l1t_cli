"""
    setup:   Used to setup things.
        Usage:
            setup <thing to setup>
"""
import logging
import os
from hepshell import HEP_PROJECT_ROOT

from .. import Command as C

LOG = logging.getLogger(__name__)
WORKSPACE = os.path.join(HEP_PROJECT_ROOT, 'workspace')


class Command(C):

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)

    def run(self, args, variables):
        self.__prepare(args, variables)
        self.__text = "NOT IMPLEMENTED"

        return True
