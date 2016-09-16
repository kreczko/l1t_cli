"""
    run macros:
        The l11 macros to create various performance plots for the L1 trigger.

        Usage:
            run macros [macro name]
"""
import logging
import os
from hepshell import HEP_PROJECT_ROOT

from .. import Command as C

from l1t_cli.setup import WORKSPACE, CMSSW_BASE, CMSSW_SRC

LOG = logging.getLogger(__name__)

MACRO_GIT_URL = 'https://github.com/kreczko/l1t-macros.git'
MACRO_DST = os.path.join(CMSSW_SRC, 'l1t_macros')


class Command(C):

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)

    def run(self, args, variables):
        self.__prepare(args, variables)
        self.__text = ''

        if not self.__check_setup():
            self.__setup()

        code = self.__run()

        if code != 0:
            # something went wrong
            return False

        return True

    def __check_setup(self):

        has_cmssw = os.path.exists(CMSSW_BASE)
        if not has_cmssw:
            LOG.warn('Could not find {0}'.format(CMSSW_BASE))

        has_macros = os.path.exists(MACRO_DST)
        if not has_macros:
            LOG.warn('Could not find {0}'.format(MACRO_DST))

        return has_cmssw and has_macros

    def __setup(self):
        from l1t_cli.commands.setup.cmssw import Command as CMSSW
        setup_cmssw = CMSSW()
        # using defaults
        setup_cmssw.run([], {})

        command = 'git clone {source} {destination}'.format(
            source=MACRO_GIT_URL, destination=MACRO_DST)

        from l1t_cli.commands.run import run_within_cmssw
        rc, _, _ = run_within_cmssw(command, logger=LOG)

        return rc

    def __run(self):
        from l1t_cli.commands.run import run_within_cmssw
        macro = os.path.join(MACRO_DST, 'makeRates.cxx')
        LOG.debug('Running {0}'.format(macro))
        command = 'root -l -b -q {0}'.format(macro)
        rc, _, _ = run_within_cmssw(command, logger=LOG)
        return rc
