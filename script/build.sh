#!/bin/bash
source ${BASH_SOURCE%/*}/clean.sh
# Run in browser:
#poetry run pdoc python_bunny_mq --logo https://raw.githubusercontent.com/tangledpath/python-bunny-mq/master/bunny.png --favicon https://raw.githubusercontent.com/tangledpath/python-bunny-mq/master/bunny-sm.png
poetry run pdoc python_bunny_mq -o ./docs --logo https://raw.githubusercontent.com/tangledpath/python-bunny-mq/master/pao.png --favicon https://raw.githubusercontent.com/tangledpath/python-bunny-mq/master/bunny-sm.png
poetry build
