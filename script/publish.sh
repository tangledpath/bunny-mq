#!/bin/bash
poetry publish --build -u __token__ -p $PYPI_TOKEN

echo "Remember to tag:"
echo 'git tag -a v0.1.1 -m "Version 0.1.1 - renamed project for compatibility."'
echo 'git push origin v0.1.1'
