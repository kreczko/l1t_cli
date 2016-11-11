"""
    setup l1toffline:
        Sets 
        Usage:
            setup
"""
import logging
import os
import hepshell
from l1t_cli.setup import INTEGRATION_TAG

LOG = logging.getLogger(__name__)


class Command(hepshell.Command):

    DEFAULTS = {

    }

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)

    def run(self, args, variables):
        self.__prepare(args, variables)
        
        from l1t_cli.commands.get.latest.integration.tag import Command as Lit
        versions_and_tags = Lit.get_versions_and_tags()
        latest_tag = Lit.get_latest_tag(versions_and_tags)

        if latest_tag != INTEGRATION_TAG:
            LOG.warn('Using integration tag (ITag) {0} but the latest tag is {1}'.format(
                INTEGRATION_TAG, latest_tag))
            LOG.warn('If this iTag is not desired, please update setup.json')

        commands = [
            'git cms-init',
            'git remote add cms-l1t-offline https://github.com/cms-l1t-offline/cmssw.git',
            'git fetch cms-l1t-offline',
            'git cms-merge-topic --unsafe cms-l1t-offline:{0}'.format(
                INTEGRATION_TAG),
            'scram b jobs=2',
        ]

        from l1t_cli.commands.run import run_within_cmssw
        for command in commands:
            run_within_cmssw(command, logger=LOG)

        return True
