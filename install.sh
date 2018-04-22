#!/bin/bash

set -e

if ! command -v python > /dev/null; then
    echo "Please install Python 2 and then run this script... exiting"
    exit 1
fi

if ! command -v pip > /dev/null && ! command -v pip2 > /dev/null; then
    echo "Please install pip and then run this script... exiting"
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

# modified from Gentle's install script
###################################
echo "Installing dependencies..."

# install OS-specific dependencies
if [[ "$OSTYPE" == "linux-gnu" ]]; then
	sudo apt-get update -qq
	sudo apt-get install -y zlib1g-dev automake autoconf git \
		libtool subversion libatlas3-base python-pip \
		python-dev wget unzip
	sudo apt-get install -y ffmpeg || echo -n  "\n\nYou have to install ffmpeg from a PPA or from https://ffmpeg.org before you can run gentle\n\n"
elif [[ "$OSTYPE" == "darwin"* ]]; then
	brew list ffmpeg || brew install ffmpeg
	brew list libtool || brew install libtool
	brew list automake || brew install automake
	brew list autoconf || brew install autoconf
	brew list wget || brew install wget
fi
###################################

# install dependencies and Kaldi
(cd gentle/ext && sudo ./install_kaldi.sh)

# load models
(cd gentle && sudo ./install_models.sh && cd ext && make depend && make)

# install Python requirements
pip install pydub || pip2 install pydub
(cd gentle && pip install . || pip2 install .)

# deal with Ubuntu 14.04 ffmpeg issues
if ! command -v ffmpeg > /dev/null && [[ "$OSTYPE" == "linux-gnu" ]]; then
    sudo add-apt-repository -y ppa:mc3man/trusty-media
    sudo apt-get -y update
    sudo apt-get -y install ffmpeg
fi

# taken from https://stackoverflow.com/a/246128
CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# add paths to profile
echo "export PYTHONPATH=$CURRENT_DIR:$CURRENT_DIR/gentle:$CURRENT_DIR/gentle/gentle:${PYTHONPATH}" >> ~/.profile