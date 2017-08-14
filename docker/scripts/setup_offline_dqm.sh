#!/bin/bash
echo "Setting up DQM Offline"
cd ${PROJECTPATH}
source /cvmfs/cms.cern.ch/cmsset_default.sh

if [ ! -d ${PROJECTPATH}/${CMSSW_VERSION} ]
then
  scram p ${CMSSW_VERSION}
fi
cd ${CMSSW_VERSION}/src
eval `/cvmfs/cms.cern.ch/common/scram runtime -sh`
if [ ! -d DQMOffline/L1Trigger ]
then
  git cms-addpkg DQMOffline/L1Trigger
fi

echo "Finished setup"
