#!/bin/bash

set -e

if ! [ -f /usr/share/xsessions/qlite.desktop ]; then
    sudo apt-get install \
        python3.4-venv python3-pip \
        libxcb-render0-dev libffi-dev libcairo2 libpangocairo-1.0-0
    sudo cp qlite.desktop /usr/share/xsessions/qlite.desktop
fi

if ! [ -d venv ]; then
    /usr/bin/python3 -m venv --system-site-packages venv
fi

source venv/bin/activate

pip="venv/bin/python -m pip"

$pip install -U pip
$pip install -U uvloop || true
$pip install -Ur requirements.txt

