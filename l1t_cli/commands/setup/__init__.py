"""
    setup:   Sets up the workspace
        Usage:
            setup
"""
import logging
import os
from hepshell import HEP_PROJECT_ROOT

from .. import Command as C

LOG = logging.getLogger(__name__)
WORKSPACE = os.path.join(HEP_PROJECT_ROOT, 'workspace')
CACHE = os.path.join(WORKSPACE, 'cache')
LOGDIR = os.path.join(WORKSPACE, 'log')
TMPDIR = os.path.join(WORKSPACE, 'tmp')
RESULTDIR = os.path.join(WORKSPACE, 'results')


class Command(C):

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)

    def run(self, args, variables):
        self.__prepare(args, variables)
        for path in [WORKSPACE, CACHE, LOGDIR, TMPDIR]:
            if not os.path.exists(path):
                LOG.debug("Creating path {0}".format(path))
                os.mkdir(path)

        return True
