import os
import json
from l1t_cli import HEP_PROJECT_ROOT

WORKSPACE = os.path.join(HEP_PROJECT_ROOT, 'workspace')
CACHE = os.path.join(WORKSPACE, 'cache')
LOGDIR = os.path.join(WORKSPACE, 'log')
TMPDIR = os.path.join(WORKSPACE, 'tmp')
RESULTDIR = os.path.join(WORKSPACE, 'results')
ACTIVE_CMSSW = os.path.join(WORKSPACE, 'current')


def read_setup():
    # load initial setup
    setup_file = os.path.join(HEP_PROJECT_ROOT, 'setup.json')
    with open(setup_file) as setup_file:
        setup = json.load(setup_file)
    return setup

SETUP = read_setup()
SCRAM_ARCH = SETUP['scram_arch']
CMSSW_VERSION = SETUP['cmssw_version']
CMSSW_BASE = os.path.join(WORKSPACE, CMSSW_VERSION)
CMSSW_SRC = os.path.join(CMSSW_BASE, 'src')
INTEGRATION_TAG = SETUP['integration_tag']
