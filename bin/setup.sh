#!/bin/bash

if [ "x${BASH_ARGV[0]}" = "x" ]; then
    if [ ! -f bin/setup.sh ]; then
        echo ERROR: must "cd where/project/is" before calling ". bin/setup.sh" for this version of bash!
        HEP_PROJECT_ROOT=; export HEP_PROJECT_ROOT
        return 1
    fi
    HEP_PROJECT_ROOT="$PWD"; export HEP_PROJECT_ROOT
else
    # get param to "."
    envscript=$(dirname ${BASH_ARGV[0]})
    HEP_PROJECT_ROOT=$(cd ${envscript}/..;pwd); export HEP_PROJECT_ROOT
fi

if [ ! -d "${HEP_PROJECT_ROOT}/external" ] ; then
	mkdir ${HEP_PROJECT_ROOT}/external
fi

if [ ! -d "${HEP_PROJECT_ROOT}/external/miniconda" ] ; then
	wget -nv http://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh -O miniconda.sh
	bash miniconda.sh -b -p ${HEP_PROJECT_ROOT}/external/miniconda
	PATH=${HEP_PROJECT_ROOT}/external/miniconda/bin:$PATH; export PATH
	rm -f miniconda.sh
	conda update conda -y
	conda update pip -y
	pip install -U python-cjson
fi

pip install -U git+https://github.com/kreczko/hepshell.git

echo "Please 'source bin/env.sh' now"
