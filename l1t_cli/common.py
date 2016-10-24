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
