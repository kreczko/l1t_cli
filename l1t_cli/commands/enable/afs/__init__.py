"""
    enable afs:
        Enables CERN AFS in the Vagrant box. Does not work elsewhere.

        Usage:
            enable AFS
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

    @time_function('setup dqm gui', LOG)
    def run(self, args, variables):
        self.__prepare(args, variables)
        commands = [
            'sudo mkdir /afs',
            'sudo /sbin/chkconfig afs on',
            'sudo /sbin/service afs start',
        ]

        if not self.__can_run():
            LOG.error('This command can only run on the Vagrant box!')
            return False

        from hepshell.interpreter import call
        for command in commands:
            call(command, logger=LOG, shell=True)

        return True

    def __can_run(self):
        is_vagrant = getpass.getuser() == 'vagrant'
        no_afs = not os.path.exists('/afs')
        if not no_afs:
            LOG.warn('/afs already exists!s')

        return is_vagrant and no_afs
