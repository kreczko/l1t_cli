FROM kreczko/centos6

ENV INSTALL_DIR=/data/srv
ENV CODE_DIR /code
ENV DQM_TAG 'HG1610a'
ENV SCRAM_ARCH 'slc6_amd64_gcc493'
EXPOSE 8060

RUN yum update -y -q && yum install -y -q \
  compat-libstdc++-33 \
  compat-readline5 \
  e2fsprogs \
  e2fsprogs-libs \
  fontconfig \
  freetype \
  git \
  hostname \
  mesa-libGL \
  mesa-libGLU \
  perl-ExtUtils-Embed \
  libICE \
  libSM \
  libX11 \
  libXcursor \
  libXext \
  libXft \
  libXi \
  libXinerama \
  libXmu \
  libXpm \
  libXrandr \
  libXrender \
  tcl \
  tcsh \
  tk \
  zsh \
  && yum clean all -y

RUN useradd dqmgui && \
    install -o dqmgui -d /data

RUN mkdir -p ${CODE_DIR}; chown dqmgui ${CODE_DIR}
USER dqmgui
RUN mkdir -p ${INSTALL_DIR};

WORKDIR ${CODE_DIR}

RUN git clone git://github.com/dmwm/deployment.git ${CODE_DIR} && \
    cd ${CODE_DIR} && \
    git reset --hard ${DQM_TAG}

COPY docker/scripts/setup_dqm_gui.sh /scripts/setup_dqm_gui.sh
RUN source /scripts/setup_dqm_gui.sh

COPY docker/scripts/run_dqm_gui.sh /scripts/run_dqm_gui.sh
CMD source /scripts/run_dqm_gui.sh && \
    sleep 60 && \
    tail -f ${INSTALL_DIR}/logs/dqmgui/dev/collector-*.log
