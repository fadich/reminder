#!/usr/bin/env bash

cd lib
python setup.py sdist
pip install dist/*
cd ..

pip install -r requirements.txt

echo
echo 'To start the server app, execute:'
echo
echo '  reminder-dev-server SERVICE_NAME'
echo
