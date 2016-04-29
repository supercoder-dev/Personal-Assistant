FROM debian:8

MAINTAINER Pavel Trutman <pavel.trutman@fel.cvut.cz>

RUN apt-get update && \
    apt-get install -y apt-utils \
                       debconf-utils
# Git
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y git \
                                                      curl && \
    curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y git-lfs && \
    git lfs install

# Ansible
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y ansible

WORKDIR /root

# clone application
RUN git clone --depth 5 https://github.com/brmson/Personal-Assistant.git

