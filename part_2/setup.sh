#!/bin/bash

rm -rf "graphs"
[[ -d "graphs" ]] || mkdir "graphs"

rm -rf "data"
[[ -d "data" ]] || mkdir "data"

pip3 install kaggle
pip3 install --user kaggle
export KAGGLE_CONFIG_DIR=.
chmod 600 ./kaggle.json

[[ -f "requirements.txt" ]] || python3 -m pip install -r requirements.txt
python3 -m pip install pymongo[srv]