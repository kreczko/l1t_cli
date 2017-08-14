FROM hepsw/cvmfs-cms

ENV CMSSW_VERSION CMSSW_9_3_0_pre3
ENV SCRAM_ARCH slc6_amd64_gcc700
ENV PROJECTPATH /project/offline-dqm
ENV USERNAME cmsuser

VOLUME /project

RUN yum update -y -q && \
  yum install -y -q \
  git \
  glibc-devel \
  sudo && \
  yum clean all

COPY docker/scripts/setup_offline_dqm.sh /scripts/setup_offline_dqm.sh
COPY docker/scripts/run_offline_dqm.sh /scripts/run_offline_dqm.sh
COPY docker/scripts/upload_to_dqm_gui.sh /scripts/upload_to_dqm_gui.sh

ARG USERID=1000
RUN adduser -u ${USERID} ${USERNAME} && \
  echo "${USERNAME} ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/${USERNAME} && \
  chmod 0440 /etc/sudoers.d/${USERNAME} && \
  cp -p /root/.bashrc /home/${USERNAME}/. && \
  chown ${USERNAME}:${USERNAME} /home/${USERNAME}/.bashrc


RUN mkdir -p ${PROJECTPATH}/${CMSSW_VERSION}/src
WORKDIR ${PROJECTPATH}/${CMSSW_VERSION}/src

RUN echo "export CMS_LOCAL_SITE=/cvmfs/cms.cern.ch/SITECONF/T3_UK_GridPP_Cloud" > /etc/cvmfs/config.d/cms.cern.ch.conf

USER ${USERNAME}
ENV HOME /home/${USERNAME}

ENTRYPOINT sudo /usr/bin/cubied && \
  sudo mkdir -p ${PROJECTPATH} && \
  sudo chown -R ${USERNAME}:${USERNAME} ${PROJECTPATH} && \
  source /scripts/setup_offline_dqm.sh && \
  tail -f /dev/null
