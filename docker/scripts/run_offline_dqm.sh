#!/usr/bin/env bash
sample=$1
step1_outputFile="L1TOffline_L1TStage2CaloLayer2_job1_RAW2DIGI_RECO_DQM.root"
echo "Running DQM Offline for ${sample}"

source /cvmfs/cms.cern.ch/cmsset_default.sh
cd ${PROJECTPATH}/${CMSSW_VERSION}/src
eval `/cvmfs/cms.cern.ch/common/scram runtime -sh`
scram b -j4
if [ $? == 0 ]
then
  echo "Running step 1 (Filling histograms)"
  cmsRun \
    DQMOffline/L1Trigger/test/runDQMOffline_step1_L1TStage2CaloLayer2_cfg.py \
    sample=${sample} \
    maxEvents=1000 \
    outputFile=${step1_outputFile}
else
  echo "Could not compile code, aborting!"
fi

if [ $? == 0 ]
then
  echo "Running step 2 (DQM Harvesting)"
  # Due to the automatic addition of 'numEventsX' to the output file name
  # we have to adjust
  step2_inputFile=`echo ${step1_outputFile} | sed -e 's/.root/*.root/g'`
  step2_inputFile=`echo ${step2_inputFile}`
  cmsRun \
  DQMOffline/L1Trigger/test/runDQMOffline_step2_L1TStage2CaloLayer2_cfg.py \
  inputFiles=${step2_inputFile}
else
  echo "Could not run step 1, aborting!"
fi
