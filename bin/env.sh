#!/bin/bash
drop_from_path()
{
   # Assert that we got enough arguments
   if test $# -ne 2 ; then
      echo "drop_from_path: needs 2 arguments"
      return 1
   fi

   p=$1
   drop=$2

   newpath=`echo $p | sed -e "s;:${drop}:;:;g" \
                          -e "s;:${drop};;g"   \
                          -e "s;${drop}:;;g"   \
                          -e "s;${drop};;g"`
}

if [ -n "${HEP_PROJECT_ROOT}" ] ; then
   old_projectbase=${HEP_PROJECT_ROOT}
fi


if [ "x${BASH_ARGV[0]}" = "x" ]; then
    if [ ! -f bin/env.sh ]; then
        echo ERROR: must "cd where/project/is" before calling ". bin/env.sh" for this version of bash!
        HEP_PROJECT_ROOT=; export HEP_PROJECT_ROOT
        return 1
    fi
    HEP_PROJECT_ROOT="$PWD"; export HEP_PROJECT_ROOT
else
    # get param to "."
    envscript=$(dirname ${BASH_ARGV[0]})
    HEP_PROJECT_ROOT=$(cd ${envscript}/..;pwd); export HEP_PROJECT_ROOT
fi

if [ -n "${old_projectbase}" ] ; then
   if [ -n "${PATH}" ]; then
      drop_from_path "$PATH" ${old_projectbase}/bin
      drop_from_path "$PATH" ${old_projectbase}/external/miniconda/bin
      PATH=$newpath
   fi
   if [ -n "${PYTHONPATH}" ]; then
      drop_from_path $PYTHONPATH ${old_projectbase}
      PYTHONPATH=$newpath
   fi
fi

if [ -z "${PATH}" ]; then
   PATH=$HEP_PROJECT_ROOT/bin; export PATH
else
   PATH=$HEP_PROJECT_ROOT/bin:$PATH; export PATH
fi

if [ -z "${PYTHONPATH}" ]; then
   PYTHONPATH=$HEP_PROJECT_ROOT; export PYTHONPATH
else
   PYTHONPATH=$HEP_PROJECT_ROOT:$PYTHONPATH; export PYTHONPATH
fi

unset old_projectbase
unset envscript

# for CMSSW
if [ -f /cvmfs/cms.cern.ch/cmsset_default.sh ]; then
	source /cvmfs/cms.cern.ch/cmsset_default.sh
	export CMSSW_GIT_REFERENCE=/cvmfs/cms.cern.ch/cmssw.git
fi

# CRAB submission
# https://twiki.cern.ch/twiki/bin/view/CMSPublic/CRAB3Releases#Improvements_enhancements_change
if [ -f /cvmfs/cms.cern.ch/crab3/crab.sh ]; then
	source /cvmfs/cms.cern.ch/crab3/crab.sh
fi

# for grid tools
vomsInfo=`which voms-proxy-info` &> /dev/null
if [ "$vomsInfo" = "" ]; then
  if [ -f /cvmfs/grid.cern.ch/etc/profile.d/setup-cvmfs-ui.sh ]; then
	source /cvmfs/grid.cern.ch/etc/profile.d/setup-cvmfs-ui.sh
  else
    echo "Cannot find voms-proxy-info nor setup-cvmfs-ui.sh"
  fi
fi

# miniconda setup for modern python and additional python packages
if [ ! -d "${HEP_PROJECT_ROOT}/external" ] ; then
	mkdir ${HEP_PROJECT_ROOT}/external
fi

PLATFORM=`python -mplatform`

if [ ! -d "${HEP_PROJECT_ROOT}/external/miniconda" ] ; then
	wget -nv http://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh -O miniconda.sh
	bash miniconda.sh -b -p ${HEP_PROJECT_ROOT}/external/miniconda
	PATH=${HEP_PROJECT_ROOT}/external/miniconda/bin:$PATH; export PATH
	rm -f miniconda.sh
	conda update conda -y
	conda update pip -y
	conda create --name l1t python=2.7 -y
	source activate l1t
	# python modules
	pip install -U python-cjson nose
	if [[ $PLATFORM == *"redhat"* ]]; then
		PYCURL_SSL_LIBRARY=nss pip install --compile pycurl --global-option='--with-nss'
	fi
	if [[ $PLATFORM == *"debian"* ]]; then
		PYCURL_SSL_LIBRARY=openssl pip install --compile pycurl --global-option='--with-openssl'
	fi
	pip install -U git+https://github.com/kreczko/hepshell.git
	
	conda clean -t -y
else
	PATH=${HEP_PROJECT_ROOT}/external/miniconda/bin:$PATH; export PATH
	source activate l1t
fi

l1t setup
