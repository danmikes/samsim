#!/bin/bash
rm -rf .venv
python3.9 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install pip-tools
pip-compile requirements.in
pip install -r requirements.txt
