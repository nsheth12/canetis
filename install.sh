#!/bin/bash

# set -e

if ! command -v python > /dev/null; then
    echo "Please install Python 2 and then run this script... exiting"
    exit 1
fi

if ! command -v pip > /dev/null; then
    echo "Please install pip for Python 2 and then run this script... exiting"
    exit 1
fi

if [[ "$OSTYPE" == "linux-gnu" ]]; then
    apt-get install git
elif [[ "$OSTYPE" == "darwin"* ]]; then
    if command -v brew > /dev/null; then
        brew install git
    else
        echo >&2 "Please install homebrew and then run this install script... exiting"
        exit 1
    fi
fi

pip install pydub
git clone https://github.com/lowerquality/gentle.git
rm -rf gentle/.git
(cd gentle && ./install.sh)
echo "export PYTHONPATH=gentle:${PYTHONPATH}" >> ~/.bashrc
echo "export PYTHONPATH=gentle/gentle:${PYTHONPATH}" >> ~/.bashrc
