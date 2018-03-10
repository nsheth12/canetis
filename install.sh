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

sudo pip install pydub
rm -rf .git
git clone https://github.com/lowerquality/gentle.git
(cd gentle && sudo ./install.sh)

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