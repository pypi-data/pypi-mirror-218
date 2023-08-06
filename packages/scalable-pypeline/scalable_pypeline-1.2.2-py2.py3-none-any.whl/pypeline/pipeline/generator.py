""" Utilities for running and managing tasks inside pipelines.
"""
import logging

from celery import signature, chord, chain
from pypeline.utils.graph_utils import get_chainable_tasks
from pypeline.utils.config_utils import retrieve_latest_pipeline_config
from pypeline.utils.task_utils import PipelineRunWrapper, get_task_signature
from pypeline.constants import DEFAULT_TASK_TTL, DEFAULT_MAX_RETRY, \
    DEFAULT_REGULATOR_TASK, CHAIN_FAILURE_MSG, CHAIN_SUCCESS_MSG, \
    DEFAULT_SUCCESS_TASK
from pypeline.pipeline_config_schema import PipelineConfigValidator


logger = logging.getLogger(__name__)


class PipelineGenerator(object):
    """ Allows an API endpoint to generate a functional pipeline based on the
        requested pipeline id. Allows API to then issue the tasks asynchronously
        to initiate the pipeline. Thereafter, celery will monitor status and
        handle success/failure modes so the API web worker can return
        immediately.

        The primary purpose is to unpack the pipeline config, create the
        requisite cached entities to track pipeline progress, and apply the
        chained pipeline tasks asynchronously so Celery can take over.

        Usage:
            gen = PipelineGenerator(pipeline_id)
            chain = gen.generate_chain()
            chain.on_error(custom_error_task.s())  # Optional add error handling
            chain.delay()
    """
    def __init__(self,
                 pipeline_id: str,
                 access_key: str = None,
                 execution_id: str = None,
                 queue: str = None,
                 default_task_ttl: int = None,
                 regulator_queue: str = None,
                 regulator_task: str = None,
                 success_queue: str = None,
                 success_task: str = None,
                 default_max_retry: int = None,
                 retry_backoff: int = None,
                 retry_jitter: bool = None,
                 retry_backoff_max: int = None,
                 chain_payload: dict = None):
        super().__init__()
        self.pipeline_id = pipeline_id
        self.access_key = access_key

        pipeline_config_api_resp = retrieve_latest_pipeline_config(
            pipeline_id=self.pipeline_id, access_key=self.access_key)

        if pipeline_config_api_resp is None:
            raise ValueError("Unable to load Pipeline Configuration for "
                             f"pipeline id: {self.pipeline_id} ...")

        # The only part of the API response used for any 'pipeline config'
        # is the `config` key. The API nests it under `config` to preserve
        # ability to add additional detail at a later date.
        self.pipeline_config = pipeline_config_api_resp.get('config', {})
        schema_version = pipeline_config_api_resp.get('schemaVersion')
        PipelineConfigValidator(config_dict=self.pipeline_config,
                                schema_version=schema_version)

        self.execution_id = execution_id  # UUID string
        self.good_to_go = False  # Indicates initialization/loading success
        self.loading_message = None  # Allows access to success/error messages
        self.is_retry = False if self.execution_id is None else True

        self.default_max_retry = default_max_retry \
            if default_max_retry is not None else \
            self.pipeline_config['metadata'].get('maxRetry', DEFAULT_MAX_RETRY)
        self.retry_backoff = retry_backoff \
            if retry_backoff is not None else \
            self.pipeline_config['metadata'].get('retryBackoff', 3)
        self.retry_backoff_max = retry_backoff \
            if retry_backoff_max is not None else \
            self.pipeline_config['metadata'].get('retryBackoffMax', 600)
        self.retry_jitter = retry_jitter \
            if retry_jitter is not None else \
            self.pipeline_config['metadata'].get('retryJitter', False)

        # Queue on which to place tasks by default and default TTL per task
        # These can be overridden in PipelineConfig.config['taskDefinitions']
        self.queue = queue \
            if queue is not None \
            else self.pipeline_config['metadata']['queue']
        self.default_task_ttl = default_task_ttl \
            if default_task_ttl is not None else \
            self.pipeline_config['metadata'].get('maxTtl', DEFAULT_TASK_TTL)

        # See docstring in self._get_regulator()
        self.regulator_queue = regulator_queue \
            if regulator_queue is not None \
            else self.pipeline_config['metadata']['queue']
        self.regulator_task = regulator_task\
            if regulator_task is not None else DEFAULT_REGULATOR_TASK

        # See docstring in self._get_success_task()
        self.success_queue = success_queue \
            if success_queue is not None \
            else self.pipeline_config['metadata']['queue']
        self.success_task = success_task\
            if success_task is not None else DEFAULT_SUCCESS_TASK

        # Optional data to pass to each step in chain
        self.chain_payload = chain_payload\
            if chain_payload is not None else {}

        self.pipeline_wrapper = None  # Allows access to the PipelineRunWrapper
        self.chain = None  # Must be intentionally built with generate_chain()

        try:
            # Generate our wrapper for this pipeline_id / execution_id
            self.pipeline_wrapper = PipelineRunWrapper(
                pipeline_id=self.pipeline_id,
                pipeline_config=self.pipeline_config,
                execution_id=self.execution_id,
                max_ttl=self.default_task_ttl,
                max_retry=self.default_max_retry,
                chain_payload=self.chain_payload)

            # Loads pipeline config from remote or cache if it's already there
            # `is_retry` will be True for any PipelineGenerator instantiated
            # with an execution_id. This flag helps the wrapper increment the
            # retry count and determine if this should be deadlettered.
            # This step also saves the valid/initialized run wrapper to cache.
            self.pipeline_wrapper.load(is_retry=self.is_retry)

            # Set all variables that were established from the run wrapper
            # initialization. Notably, default_task_ttl can be overloaded
            # if the pipeline config has an explicit maxTtl set in metadata.
            self.good_to_go = self.pipeline_wrapper.good_to_go
            self.loading_message = self.pipeline_wrapper.loading_message
            self.execution_id = self.pipeline_wrapper.execution_id

        except Exception as e:
            fail_msg = "Failed to load Pipeline for id {} ... {}".format(
                self.pipeline_id, e)
            self.loading_message = fail_msg
            logger.error(fail_msg)
            raise e

    def _get_regulator(self):
        """ Create a chain regulator celery task signature.

            For a chain(), if each element is a group() then celery does not
            properly adhere to the chain elements occurring sequentially. If you
            insert a task that is not a group() in between, though, then the
            chain operates as expected.
        """
        return signature(self.regulator_task,
                         queue=self.regulator_queue,
                         immutable=True)

    def _get_success_task(self):
        """ A final 'success' task that's added to the end of every pipeline.

            This stores the 'success' state in the cached result. Users can
            set other values by using TaskRunner().save_result()
        """
        return get_task_signature(task_path=self.success_task,
                                  queue=self.success_queue,
                                  pipeline_id=self.pipeline_id,
                                  execution_id=self.execution_id)

    def _get_signature(self, node):
        """ Create a celery task signature based on a graph node.
        """
        metadata = self.pipeline_config['metadata']
        node_config = self.pipeline_config['taskDefinitions'][node]

        # Node config takes precedence, pipeline metadata as default
        queue = node_config.get('queue', metadata['queue'])
        max_ttl = node_config.get('maxTtl', metadata.get('maxTtl', None))

        # Ensures task signatures include requisite information to retrieve
        # PipelineRunWrapper from cache using the pipeline id, and execution id.
        # We set immutable=True to ensure each client task can be defined
        # with this specific signature (event)
        # http://docs.celeryproject.org/en/master/userguide/canvas.html#immutability
        return get_task_signature(task_path=node_config.get('handler'),
                                  queue=queue,
                                  access_key=self.access_key,
                                  pipeline_id=self.pipeline_id,
                                  execution_id=self.execution_id,
                                  max_ttl=max_ttl,
                                  immutable=True,
                                  task_config=node_config)

    def generate_chain(self):
        """ Generate the full pipeline chain.
        """
        logger.debug(f'Starting Pipeline {self.pipeline_id}')

        if not self.good_to_go:
            logger.info("Chain deemed to be not good to go.")
            if self.loading_message is None:
                self.loading_message = CHAIN_FAILURE_MSG
            return None

        try:
            # Create the task chain such that all concurrent tasks are grouped
            # and all high level node groups are run serially
            G = self.pipeline_wrapper.execution_graph

            total_tasks = 0
            pipeline_chain = []
            chainable_tasks = get_chainable_tasks(G, None, [])

            # Current chord+chain solution based on
            # https://stackoverflow.com/questions/15123772/celery-chaining-groups-and-subtasks-out-of-order-execution
            # Look also at last comment from Nov 7, 2017 here
            # https://github.com/celery/celery/issues/3597
            # Big outstanding bug in Celery related to failures in chords that
            # results in really nasty log output. See
            # https://github.com/celery/celery/issues/4834
            for i, node_group in enumerate(chainable_tasks):
                total_tasks += len(node_group)
                this_group = []
                for node in node_group:
                    node_signature = self._get_signature(node)
                    this_group.append(node_signature)

                if len(this_group) <= 1:
                    this_group.append(self._get_regulator())

                the_chord = chord(header=this_group,
                                  body=self._get_regulator())

                pipeline_chain.append(the_chord)

            # Add a 'finished/success' task to the end of all pipelines
            pipeline_chain.append(
                chord(header=self._get_success_task(),
                      body=self._get_regulator()))

            the_chain = chain(*pipeline_chain)

            self.loading_message = CHAIN_SUCCESS_MSG

            self.chain = the_chain
        except Exception as e:
            self.loading_message = CHAIN_FAILURE_MSG + " {}".format(e)
            logger.exception(e)
            the_chain = None

        self.chain = the_chain

        return the_chain
