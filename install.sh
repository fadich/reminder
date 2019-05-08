#!/usr/bin/env bash

REMINDER_VERSION=$(pip show reminder | grep "Version: " | cut -d':' -f 2 | sed -e s/^[[:space:]]*//)

cd lib
python setup.py sdist
pip install dist/reminder-0.1.0.tar.gz
cd ..

pip install -r server/requirements.txt
