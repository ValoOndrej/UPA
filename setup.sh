#!/bin/bash

rm -rf "data"
[[ -d "data" ]] || mkdir "data"

[[ -f "requirements.txt" ]] || python3 -m pip install -r requirements.txt
python3 -m pip install pymongo[srv]