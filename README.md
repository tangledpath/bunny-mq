# Python Bunny MQ
Python-based package that implements a no-dependency, ultra-lightweight intra-process message queue.  This works inside a single process.  
* This is useful when you need a lightweight pub-sub system
* For example, the author is using it in development to send message to local handlers.  These are deployed to AWS and are invoked as a lambda function via SQS.   

<p>
  <img src="https://raw.githubusercontent.com/tangledpath/python-bunny-mq/master/bunny.png" align="left" width="512"/>
</p>
<p>&nbsp</p>
<p>&nbsp</p>
<p>&nbsp</p>
<p>&nbsp</p>
<p>&nbsp</p>
<p>&nbsp</p>
<p>&nbsp</p>
<p>&nbsp</p>
<p>&nbsp</p>
<p>&nbsp</p>
<p>&nbsp</p>
<p>&nbsp</p>
<p>&nbsp</p>

## Homepage
https://pypi.org/project/python-bunny-mq/

## GitHub
https://github.com/tangledpath/python-bunny-mq

## Documentation
https://tangledpath.github.io/python-bunny-mq

## Installation
pip install python-bunny-mq

## Getting started
## Development
### Linting 
Linting is done via autopep8
```bash
script/lint.sh
```

### Documentation
```
# Shows in browser
poetry run pdoc python_bunny_mq/
# Generates to ./docs
script/build.sh
```

### Testing
```bash
  clear; pytest
```

### Building and Publishing
#### Building
```bash
scriopt/build.sh
```
#### Publishing
Note: `--build` flag build before publishing
```bash
script/publish.sh
# poetry publish --build -u __token__ -p $PYPI_TOKEN
```
