#!/bin/bash

set -e

if ! command -v python > /dev/null; then
    echo "Please install Python 2 and then run this script... exiting"
    exit 1
fi

if ! command -v pip > /dev/null; then
    echo "Please install pip for Python 2 and then run this script... exiting"
    exit 1
fi

if ! command -v git > /dev/null; then
    echo "Please install git and then run this script... exiting"
    exit 1
fi

# initialize Gentle submodule
git submodule init
git submodule update

# initialize Kaldi submodule inside of Gentle
(cd gentle && git submodule init && git submodule update)

# install dependencies and Kaldi
(cd gentle && ./install_deps.sh && cd ext && sudo ./install_kaldi.sh)

# load models
(cd gentle && sudo ./install_models.sh && cd ext && make depend && make)

pip install pydub

# deal with Ubuntu 14.04 ffmpeg issues
if ! command -v ffmpeg > /dev/null && [[ "$OSTYPE" == "linux-gnu" ]]; then
    sudo add-apt-repository -y ppa:mc3man/trusty-media
    sudo apt-get -y update
    sudo apt-get -y install ffmpeg
fi

# taken from https://stackoverflow.com/a/246128
CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# a hacky initial solution
echo "export PYTHONPATH=$CURRENT_DIR:$CURRENT_DIR/gentle:$CURRENT_DIR/gentle/gentle:${PYTHONPATH}" >> ~/.profile