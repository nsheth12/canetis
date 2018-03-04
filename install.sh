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

pip install pydub
rm -rf .git
git clone https://github.com/lowerquality/gentle.git
(cd gentle && ./install.sh)
echo "export PYTHONPATH=gentle:${PYTHONPATH}" >> ~/.bashrc
echo "export PYTHONPATH=gentle/gentle:${PYTHONPATH}" >> ~/.bashrc
