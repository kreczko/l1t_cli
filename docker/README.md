# Docker for L1T development (draft)
While most of the CMS services and software will run on dedicated Scientific
Linux 6 or CentOS 7 machines, the developers OS might be very different.
In order to facilitate code development on local hardware, this project provides
several [docker containers](https://www.docker.com/) for the CMSSW software and
DQM GUI. The whole setup (CMSSW + DQM GUI) is run by two [docker-compose](https://docs.docker.com/compose/)
commands:
 1. `docker-compose up -d` to start the services
 2. `docker-compose down` to shut them down

After start the DQM GUI will become available under [http://localhost:8060/dqm/dev](http://localhost:8060/dqm/dev)
(start-up time is 30-60s) and the current directory will be available in the CMSSW container (more later).


## Prerequisites
 1. Install [Docker](https://www.docker.com)
 2. Install docker-compose: `pip install -U docker-compose`

## Development workflow

### Before starting the containers
 - create folders
    ```shell
    mkdir -p workspace/offline-dqm
    mkdir -p /tmp/cvmfs-dqm
    mkdir -p data
    ```
 - check user ID (if change needed rebuild docker `docker-compose build`)


### Running the code

### Uploading to DQM GUI

# offline-dqm
```shell
mkdir -p workspace/offline-dqm
mkdir -p /tmp/cvmfs-dqm
mkdir -p data
docker-compose up -d

# to attach (interactive shell within the container)
docker exec -ti l1tcli_dqm-gui_1 bash

# just a one-off (e.g. to restart DQM GUI after code changes)
docker exec -ti l1tcli_dqm-gui_1 bash -c 'source /scripts/run_dqm_gui.sh'



#
docker exec -ti l1tcli_offline-dqm_1 bash -c 'source /scripts/run_offline_dqm.sh'
```


## Data
# Datasets
For EG:
 - dataset=/DoubleEG/Run2016D-ZElectron-23Sep2016-v1/RAW-RECO

For Jet & Sums:
 - /SingleMuon/Run2016D-ZMu-23Sep2016-v1/RAW-RECO
