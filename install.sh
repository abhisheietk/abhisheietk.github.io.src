#!/usr/bin/bash

pip3 install pelican typogrify webassets

git submodule update --init --recursive --progress --jobs=10
PYTHONPATH=. make html
