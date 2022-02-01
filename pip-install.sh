#!/bin/bash

source venv/bin/activate
pip-compile requirements/requirements.in

echo "Development / Production [D/P]?"
read VAR

if [[ "$VAR" == "D" ]]
then
  echo "Development"
  pip-compile requirements/requirements-dev.in
  pip-sync requirements/requirements.txt requirements/requirements-dev.txt
elif [[ "$VAR" == "P" ]]
then
  echo "Production"
  pip-compile requirements/requirements-prod.in
  pip-sync requirements/requirements.txt requirements/requirements-prod.txt
else
  echo "Please choose from [D/P]"
fi
deactivate