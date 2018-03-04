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

# pip install pydub
# rm -rf .git
# git clone https://github.com/lowerquality/gentle.git
# (cd gentle && ./install.sh)

# taken from https://stackoverflow.com/a/246128
CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# a hacky initial solution
echo "export PYTHONPATH=$CURRENT_DIR:$CURRENT_DIR/gentle:$CURRENT_DIR/gentle/gentle:${PYTHONPATH}" >> ~/.bashrc
echo "export PYTHONPATH=$CURRENT_DIR:$CURRENT_DIR/gentle:$CURRENT_DIR/gentle/gentle:${PYTHONPATH}" >> ~/.zshrc