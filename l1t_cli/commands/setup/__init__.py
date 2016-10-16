"""
    setup:   Sets up the workspace
        Usage:
            setup
"""
import logging
import os
import hepshell


LOG = logging.getLogger(__name__)
WORKSPACE = os.path.join(hepshell.HEP_PROJECT_ROOT, 'workspace')
CACHE = os.path.join(WORKSPACE, 'cache')
LOGDIR = os.path.join(WORKSPACE, 'log')
TMPDIR = os.path.join(WORKSPACE, 'tmp')
RESULTDIR = os.path.join(WORKSPACE, 'results')


class Command(hepshell.Command):

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)

    def run(self, args, variables):
        self.__prepare(args, variables)
        for path in [WORKSPACE, CACHE, LOGDIR, TMPDIR, RESULTDIR]:
            if not os.path.exists(path):
                LOG.debug("Creating path {0}".format(path))
                os.mkdir(path)

        return True
