# Python Bunny MQ
Python-based package that implements a no-dependency, ultra-lightweight intra-process message queue.  This works inside a single process, running in a separate thread.
![](https://raw.githubusercontent.com/tangledpath/python-bunny-mq/master/bunny-sm.png)

* This is useful when you need a lightweight pub-sub system.
* Introduce intra-process decoupling without running a separate service. 
* It is backed by python's multiproducer, multiconsumer [queue](https://docs.python.org/3/library/queue.html).  


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
