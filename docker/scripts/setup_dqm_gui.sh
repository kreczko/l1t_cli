#!/bin/bash
${CODE_DIR}/Deploy -r "comp=comp.pre" -A ${SCRAM_ARCH} -R comp@${DQM_TAG} -t ${DQM_TAG} -s "prep sw post" ${INSTALL_DIR} dqmgui/bare

# mv ${INSTALL_DIR}/current/config/dqmgui{,.bak}
# ln -s ${CODE_DIR}/dqmgui ${INSTALL_DIR}/current/config/dqmgui
