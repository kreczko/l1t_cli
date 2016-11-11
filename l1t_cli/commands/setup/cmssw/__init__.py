"""
    setup cmssw:
        Sets up the CMS software in the workspace. Workspace must exist.
        
    Usage:
        setup cmssw version=<cmssw_version> [alias=<>] [--init-git]\
                    [parent_folder=<>]
        
    Parameters:
        version: The version of CMSSW to set up (e.g. CMSSW_8_0_0)
                 Default: What is defined in setup.json

        scram_arch: The architecture for the CMSSW version
                    (e.g. slc6_amd64_gcc530).
                    Default: What is defined in setup.json

        alias:    Instead of the CMSSW version (CMSSW_X_Y_Z) the project folder
                  will be set to the value of 'alias'

        parent_folder: Parent folder of the CMSSW project.
                       Default: $HEP_PROJECT_ROOT/workspace

        init-git: Prepares the CMSSW area for merging of git branches.
                  Default:true
"""
import logging
import os
import hepshell
from hepshell.interpreter import time_function

LOG = logging.getLogger(__name__)

from l1t_cli.setup import CMSSW_VERSION, WORKSPACE, SCRAM_ARCH


class Command(hepshell.Command):
    DEFAULTS = {
        'version': CMSSW_VERSION,
        'init-git': True,
        'parent_folder': WORKSPACE,
        'alias': CMSSW_VERSION,
        'scram_arch': SCRAM_ARCH,
    }

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)

    @time_function('setup cmssw', LOG)
    def run(self, args, variables):
        self.__prepare(args, variables)

        self.__version = self.__variables['version']
        self.__scram_arch = self.__variables['scram_arch']
        self.__alias = self.__variables['alias']
        if self.__alias == '':
            self.__alias = self.__version
        self.__parent_folder = self.__variables['parent_folder']
        self.__init_git = self.__variables['init-git']

        if not self.__can_run():
            return False

        commands = [
            'cd {parent_folder}',
            'export SCRAM_ARCH={scram_arch}',
            'source /cvmfs/cms.cern.ch/cmsset_default.sh',
            '/cvmfs/cms.cern.ch/common/scram project -n {alias} CMSSW {version}',
        ]
        if self.__variables['init-git']:
            commands.extend([
                'cd {alias}/src',
                'eval `/cvmfs/cms.cern.ch/common/scram runtime -sh`',
                'git cms-init',
            ])

        all_in_one = ' && '.join(commands)
        all_in_one = all_in_one.format(
            parent_folder=self.__parent_folder,
            scram_arch=self.__scram_arch,
            version=self.__version,
            alias=self.__alias,
        )

        from hepshell.interpreter import call
        call(all_in_one, logger=LOG, shell=True)

        return True

    def __can_run(self):
        if not os.path.exists(self.__parent_folder):
            LOG.error(
                'Parent folder does not exist: {0}'.format(self.__parent_folder))
            return False
        project_path = os.path.join(self.__parent_folder, self.__alias)
        if os.path.exists(project_path):
            LOG.error('CMSSW is already set up: {0}'.format(project_path))
            return False
        return True
