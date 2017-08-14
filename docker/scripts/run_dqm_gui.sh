#!/bin/bash

mv ${INSTALL_DIR}/current/config/dqmgui{,.bak}
ln -s ${CODE_DIR}/dqmgui ${INSTALL_DIR}/current/config/dqmgui

source ${INSTALL_DIR}/current/*/*/external/apt/*/etc/profile.d/init.sh
${INSTALL_DIR}/current/config/dqmgui/manage restart 'I did read documentation'
