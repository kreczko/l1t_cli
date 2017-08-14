#!/usr/bin/env bash
echo "Uploading to DQM GUI: http://localhost:8060/dqm/dev"

file_to_upload $1

source /data/srv/current/apps/dqmgui/128/etc/profile.d/env.sh

visDQMUpload http://dqm-gui:8060/dqm/dev ${file_to_upload}
