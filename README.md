# Python Arango OGM
Python-based package that implements a no-dependency, ultra-lightweight intra-process message queue.  This works inside a single process.  
* This is useful when you need a lightweight pub-sub system
* For example, the author is using it in development to send message to local handlers.  These are deployed to AWS and are invoked as a lambda function via SQS.   

<p>
  <img src="https://raw.githubusercontent.com/tangledpath/bunny-mq/master/bunny.png" align="left" width="512"/>
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
https://pypi.org/project/bunny-mq/

## GitHub
https://github.com/tangledpath/bunny-mq

## Documentation
https://tangledpath.github.io/bunny-mq

## Installation
pip install bunny-mq

## Getting started
Create a .env file at the root of your repository with the following keys; values to be adjusted for your application:

### Environment file (or production configuration/secrets):
These environment variables should be defined
```
PAO_APP_DB_NAME=your_app                    # The Arango database name for your app
PAO_APP_DB_USER=your_app                    # The Arango database username for your app
PAO_APP_DB_PASS=<ARANGO_YOUR_APP_PASSWORD>  # The Arango database password for your app
PAO_APP_PACKAGE=your_app.gdb                # The package within your app where models and migrations are built
PAO_DB_HOST=localhost                       # The DB host
PAO_DB_PORT=8529                            # The DB port
PAO_DB_ROOT_USER=root                       # The root DB username
PAO_DB_ROOT_PASS=<ARANGO_ROOT_PASSWORD>     # The root DB password
PAO_GRAPH_NAME=your_app_graph               # Name of the graph to generate from your vertices and edges
```

* Models should be in the module PAO_APP_PACKAGE.models, e.g., `your_app/gdb/models.py`
* Migrations will be generated in the package PAO_APP_PACKAGE.migrations, e.g., `your_app/gdb/migrations/`

### Initializing the database:
Create an `__init__.py` file in your application's source tree to initialize the database; causing it to inject itself into the models.  PAODatabase is a based on a singleton metaclass:
Modify as necessary:
```python
# Filename = your-app/your_app/gdb/__init__.py
import os
from dotenv import load_dotenv
from python_arango_ogm.db.pao_database import PAODatabase

# This assumes a development environment, you can add other environments; e.g., test.
# Production environments will most likely not use dotenv files:
if os.getenv('YOUR_APP_ENV', 'development') == 'development':
    load_dotenv('.env') # Or '.env.dev', '.env.test', etc....

PAODatabase()
```

In this setup, there should be a `models.py` in the your_app.gdb package.  For example, to define three models with two edges: 

```python
from python_arango_ogm.db import pao_fields
from python_arango_ogm.db.pao_edges import PAOEdgeDef
from python_arango_ogm.db.pao_model import PAOModel


class FooModel(PAOModel):
    field_int = pao_fields.IntField(index_name='field_int_idx')
    field_str = pao_fields.StrField(unique=True, index_name='field_str_idx')
    bar_edge = PAOEdgeDef("FooModel", "BarModel")


class BarModel(PAOModel):
    field_int = pao_fields.IntField(index_name='field_int_idx', required=True)
    field_str = pao_fields.StrField(unique=True, index_name='field_str_idx')


class BazModel(PAOModel):
    field_int = pao_fields.IntField(index_name='field_int_idx', unique=True, required=True)
    field_str = pao_fields.StrField(index_name='field_str_idx')
    foo_edge = PAOEdgeDef("BazModel", FooModel)
```

## Usage:
### pao-migrate CLI
* Make uncreated migrations for models: `pao-migrate make-migrations`
* Migrate the database: `pao-migrate migrate`
* Remove and Migrate the database: `pao-migrate migrate --clean`
* List migrations: `pao-migrate list-migrations`
* Rollback last migration: `pao-migrate migrate-rollback`
* Create a blank migration: `pao-migrate new-migration <MIGRATION_NAME>`
* To see help `pao-migrate --help`
* To see help for a specific command, for example: `pao-migrate migrate --help`
* All of the above commands accept an optional "--env-file" argument; useful in development and testing.  For production, you will likely not use a dotenv file, and should rely instead on environment variable set in your production environment.    

### In code
You may use your models to perform various queries and commands
**TODO**: document this more

## Development
### Linting
```bash
   ruff check . # Find linting errors
   ruff check . --fix # Auto-fix linting errors (where possible)
```

### Documentation
```
# Shows in browser
poetry run pdoc python_arango_ogm/
# Generates to ./docs
poetry run pdoc python_arango_ogm/ -o ./docs
# OR (recommended)
bin/build.sh 
```

### Testing
```bash
  clear; pytest
```

### Building and Publishing
#### Building
`poetry build`
#### Publishing
Note: `--build` flag build before publishing
`poetry publish --build -u __token__ -p $PYPI_TOKEN`
