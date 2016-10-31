import os
import logging

LOG = logging.getLogger(__name__)


def update_symlink(symlink, destination):
    '''
        Updates the destination of a symlink:
          - deletes @symlink if existing
          - creates new symlink
    '''
    if os.path.exists(symlink):
        LOG.debug('Deleting existing symlink')
        os.remove(symlink)

    os.symlink(destination, symlink)


def is_vagrant_host():
    import getpass
    import socket
    user = getpass.getuser()
    hostname = socket.gethostname()

    return user == 'vagrant' and hostname == 'localhost'
