# PypeLine

## Quickstart

1. Add `pypeline` as a dependency to your Python application
1. Install extras depending on what you are building:

1. `flask` - Convenient interface for Flask applications
1. `web` - Some standard web server dependencies we like
1. `workers` - Installs [Celery](https://docs.celeryproject.org/en/stable/getting-started/introduction.html) and [networkx](https://networkx.org/documentation/stable/index.html), which are required if using pipelines.

## Overview

PypeLines is a fork of [Sermos] (https://gitlab.com/sermos/sermos). PypeLines diverges from Sermos as a SAAS platform and is intented as a suite for job management in conjuction with or indepent from a Flask Web App. Common job management workflow's include running pipelines, scheduled tasks, and other various types of jobs. Pypelines is designed to make these systems faster and more intuitive to create for Python developers.

Under the hood we are simply extending various Celery capabilities like their existing complex workflows and make them suitable for large scale pipelines that can be run in production. To do this PypeLines uses a custom Celery configuration and a library known as [Celery-Dyrygent](https://github.com/ovh/celery-dyrygent) to help orchestrate thousands of tasks at once.

### Pypeline

-   Celery Configuration
-   Pipelines
-   CronJobs
-   APIs
-   Utilities

### Your Application

This is where all of your code lives and only has a few _requirements_:

1. It is a base application written in Python.
1. Scheduled tasks and Pipeline nodes must be Python Methods that accept
   at least one positional argument: `event`
1. A `sermos.yaml` file, which is a configuration file for running scheduled tasks and pipelines.

## Celery

Pypelines provides sensical default configurations for the use of
[Celery](http://www.celeryproject.org/). The default deployment uses RabbitMQ,
and is recommended. This library can be implemented in any other workflow
(e.g. Kafka) as desired.

There are two core aspects of Celery that pypeline handles and differ from a
standard Celery deployment.

### ChainedTask

In `celery.py` when imported it will configure Celery and also run
`GenerateCeleryTasks().generate()`, which will use the `sermos.yaml` config
to turn customer methods into decorated Celery tasks.

Part of this process includes adding `ChainedTask` as the _base_ for all of
these dynamically generated tasks.

`ChainedTask` is a Celery `Task` that injects `tools` and `event` into the
signature of all dynamically generated tasks.

### SermosScheduler

We allow users to set new scheduled / recurring tasks on-the-fly. Celery's
default `beat_scheduler` does not support this behavior and would require the
Beat process be killed/restarted upon every change. Instead, we set our
custom `sermos.celery_beat:SermosScheduler` as the `beat_scheduler`,
which takes care of watching the database for new/modified entries and reloads
dynamically.

## Workers / Tasks / Pipeline Nodes

PypeLine handles decorating the tasks, generating the correct Celery
chains, etc.

Customer code has one requirement: write a python method that accepts one
positional argument: `event`

e.g.

    def demo_pipeline_node_a(event):
        logger.info(f"RUNNING demo_pipeline_node_a: {event}")
        return

### Generators

_TODO_: This needs to be updated both in code and documentation. Leaving here
because it's valuable to update in the future.

A common task associated with processing batches of documents is generating
the list of files to process. `pypeline.generators` contains two helpful
classes to generate lists of files from S3 and from a local file system.

`S3KeyGenerator` will produce a list of object keys in S3. Example:

    gen = S3KeyGenerator('access-key', 'secret-key')
    files = gen.list_files(
        'bucket-name',
        'folder/path/',
        offset=0,
        limit=4,
        return_full_path=False
    )

`LocalKeyGenerator` will produce a list of file names on a local file system.
Example:

    gen = LocalKeyGenerator()
    files = gen.list_files('/path/to/list/')

## Testing

If you are developing pypeline and want to test this package,
install the test dependencies:

    $ pip install -e .[test]

Now, run the tests:

    $ tox
