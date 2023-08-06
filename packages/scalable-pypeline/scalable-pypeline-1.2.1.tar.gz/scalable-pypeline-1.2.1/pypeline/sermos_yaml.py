""" Definition of the `sermos.yaml` file. This is only relevant/used for
managed deployments through Sermos.ai. If self-hosting, safely disregard this
yaml format, no `sermos.yaml` is required for your application.

If using, a basic file may look like::
    serviceConfig:
        - name: sermos-worker
            registeredTasks:
                - handler: sermos_demo_client.workers.demo_worker.demo_worker_task
                - handler: sermos_demo_client.workers.demo_worker.demo_model_task

    pipelines:
        demo-pipeline:
            name: demo-pipeline
            description: Demo Pipeline.
            schemaVersion: 1
            config:
                dagAdjacency:
                    node_a:
                        - node_b
                        - node_c
                metadata:
                    maxRetry: 3
                    maxTtl: 60
                    queue: default-task-queue
                taskDefinitions:
                    node_a:
                        handler: sermos_demo_client.workers.demo_pipeline.demo_pipeline_node_a
                    node_b:
                        handler: sermos_demo_client.workers.demo_pipeline.demo_pipeline_node_b
                        queue: node-b-queue
                    node_c:
                        handler: sermos_demo_client.workers.demo_pipeline.demo_pipeline_node_c

    scheduledTasks:
        demo-model-task:
            name: Demo Model Task
            enabled: true
            config:
                scheduleType: interval
                task: sermos_demo_client.workers.demo_worker.demo_model_task
                queue: default-task-queue
                schedule:
                    every: 60
                    period: seconds
            schemaVersion: 1

"""
import re
import os
import logging
import pkg_resources
import yaml
from yaml.loader import SafeLoader
from marshmallow import Schema, fields, pre_load, EXCLUDE, INCLUDE,\
    validates_schema
from marshmallow.validate import OneOf
from marshmallow.exceptions import ValidationError
from pypeline.utils.module_utils import SermosModuleLoader, normalized_pkg_name
from pypeline.constants import SERMOS_YAML_PATH, SERMOS_CLIENT_PKG_NAME
from pypeline.pipeline_config_schema import BasePipelineSchema
from pypeline.schedule_config_schema import BaseScheduleSchema

logger = logging.getLogger(__name__)


class InvalidPackagePath(Exception):
    pass


class InvalidSermosConfig(Exception):
    pass


class MissingSermosConfig(Exception):
    pass


class ExcludeUnknownSchema(Schema):
    class Meta:
        unknown = EXCLUDE


class NameSchema(Schema):
    """ Validated name string field.
    """
    name = fields.String(
        required=True,
        description="Name for service or image. Must include "
        "only alphanumeric characters along with `_` and `-`.",
        example="my-service-name")

    @pre_load
    def validate_characters(self, item, **kwargs):
        """ Ensure name field conforms to allowed characters
        """
        valid_chars = r'^[\w\d\-\_]+$'
        if not bool(re.match(valid_chars, item['name'])):
            raise ValueError(
                f"Invalid name: {item['name']}. Only alphanumeric characters "
                "allowed along with `-` and `_`.")
        return item


class SermosRegisteredTaskDetailConfigSchema(Schema):
    handler = fields.String(
        required=True,
        description="Full path to the Method handles work / pipeline tasks.",
        example="sermos_customer_client.workers.worker_group.useful_worker")

    event = fields.Raw(
        required=False,
        unknown=INCLUDE,
        description="Arbitrary user data, passed through `event` arg in task.")


class SermosCeleryWorkerConfigSchema(Schema):
    """ Attributes for a celery worker.  This worker will run all of the
        pipelines and scheduled tasks.
    """
    registeredTasks = fields.List(
        fields.Nested(SermosRegisteredTaskDetailConfigSchema, required=True),
        required=False,
        _required=True,
        description="List of task handlers to register for to your Sermos app."
    )


class SermosServiceConfigSchema(ExcludeUnknownSchema,
                                SermosCeleryWorkerConfigSchema, NameSchema):
    """ Base service config object definition for workers.
    """
    pass


class SermosYamlSchema(ExcludeUnknownSchema):
    """ The primary `sermos.yaml` file schema. This defines all available
        properties in a valid Sermos configuration file.
    """
    serviceConfig = fields.List(
        fields.Nested(SermosServiceConfigSchema,
                      required=True,
                      description="Core service configuration."),
        description="List of workers for Sermos to manage.",
        required=True)

    pipelines = fields.Dict(keys=fields.String(),
                            values=fields.Nested(BasePipelineSchema),
                            description="List of pipelines",
                            required=False)

    scheduledTasks = fields.Dict(keys=fields.String(),
                                 values=fields.Nested(BaseScheduleSchema),
                                 description="List of scheduled tasks",
                                 required=False)

    def validate_errors(self, schema: Schema, value: dict):
        """ Run Marshmallow validate() and raise if any errors
        """
        schema = schema()
        errors = schema.validate(value)
        if len(errors.keys()) > 0:
            raise ValidationError(errors)

    @validates_schema
    def validate_schema(self, data, **kwargs):
        """ Additional validation.

            Nested fields that are not required are not validated by Marshmallow
            by default. Do a single level down of validation for now.

            imageConfig can provide *either* an install command for Sermos
            to use to build the image for customer *or* a Docker repository
            for Sermos to pull.
        """
        # Vaidate nested
        key_schema_pairs = (
            ('serviceConfig', SermosServiceConfigSchema),
        )
        for k_s in key_schema_pairs:
            val = data.get(k_s[0], None)
            if val is not None:
                if type(val) == list:
                    for v in val:
                        self.validate_errors(k_s[1], v)
                else:
                    self.validate_errors(k_s[1], val)

        # Validate the services. We list every service schema field as not
        # required in order to use them as mixins for a generic service object,
        # however, they ARE required, so validate here using the custom
        # metadata property `_required`. Default to value of `required`.
        for service in data.get('serviceConfig'):
            schema = SermosCeleryWorkerConfigSchema
            for field in schema().fields:
                try:
                    if schema().fields[field].metadata.get(
                            '_required',
                            getattr(schema().fields[field], 'required')):
                        assert field in service
                except AssertionError:
                    raise ValidationError(
                        f"`{field}` missing in worker definition.")

        # Validate unique pipeline ids
        if 'pipelines' in data:
            pipeline_ids = set()
            for pipeline_id, pipeline_data in data['pipelines'].items():
                if pipeline_id in pipeline_ids:
                    raise ValidationError("All pipeline ids must be unique!")
                pipeline_ids.add(pipeline_id)
                schema_version = pipeline_data['schemaVersion']
                PipelineSchema = \
                    BasePipelineSchema.get_by_version(schema_version)
                self.validate_errors(PipelineSchema, pipeline_data)

        # Validate unique scheduled tasks names
        if 'scheduledTasks' in data:
            task_ids = set()
            for task_id, task_data in data['scheduledTasks'].items():
                if task_id in task_ids:
                    raise ValidationError("All schedule ids must be unique!")
                task_ids.add(task_id)
                schema_version = task_data['schemaVersion']
                TaskSchema = BaseScheduleSchema.get_by_version(schema_version)
                self.validate_errors(TaskSchema, task_data)


class YamlPatternConstructor():
    """ Adds a pattern resolver + constructor to PyYaml.

        Typical/deault usage is for parsing environment variables
        in a yaml file but this can be used for any pattern you provide.

        See: https://pyyaml.org/wiki/PyYAMLDocumentation
    """
    def __init__(self,
                 env_var_pattern: str = None,
                 add_constructor: bool = True):
        self.env_var_pattern = env_var_pattern
        if self.env_var_pattern is None:
            # Default pattern is: ${VAR:default}
            self.env_var_pattern = r'^\$\{(.*)\}$'
        self.path_matcher = re.compile(self.env_var_pattern)

        if add_constructor:
            self.add_constructor()

    def _path_constructor(self, loader, node):
        """ Extract the matched value, expand env variable,
            and replace the match

            TODO: Would need to update this (specifically the parsing) if any
            pattern other than our default (or a highly compatible variation)
            is provided.
        """
        # Try to match the correct env variable pattern in this node's value
        # If the value does not match the pattern, return None (which means
        # this node will not be parsed for ENV variables and instead just
        # returned as-is).
        env_var_name = re.match(self.env_var_pattern, node.value)
        try:
            env_var_name = env_var_name.group(1)
        except AttributeError:
            return None

        # If we get down here, then the 'node.value' matches our specified
        # pattern, so try to parse. env_var_name is the value inside ${...}.
        # Split on `:`, which is our delimiter for default values.
        env_var_name_split = env_var_name.split(':')

        # Attempt to retrieve the environment variable...from the environment
        env_var = os.environ.get(env_var_name_split[0], None)

        if env_var is None:  # Nothing found in environment
            # If a default was provided (e.g. VAR:default), return that.
            # We join anything after first element because the default
            # value might be a URL or something with a colon in it
            # which would have 'split' above
            if len(env_var_name_split) > 1:
                return ":".join(env_var_name_split[1:])
            return 'unset'  # Return 'unset' if not in environ nor default
        return env_var

    def add_constructor(self):
        """ Initialize PyYaml with ability to resolve/load environment
            variables defined in a yaml template when they exist in
            the environment.

            Add to SafeLoader in addition to standard Loader.
        """
        # Add the `!env_var` tag to any scalar (value) that matches the
        # pattern self.path_matcher. This allows the template to be much more
        # intuitive vs needing to add !env_var to the beginning of each value
        yaml.add_implicit_resolver('!env_var', self.path_matcher)
        yaml.add_implicit_resolver('!env_var',
                                   self.path_matcher,
                                   Loader=SafeLoader)

        # Add constructor for the tag `!env_var`, which is a function that
        # converts a node of a YAML representation graph to a native Python
        # object.
        yaml.add_constructor('!env_var', self._path_constructor)
        yaml.add_constructor('!env_var',
                             self._path_constructor,
                             Loader=SafeLoader)


def parse_config_file(sermos_yaml: str):
    """ Parse the `sermos.yaml` file when it's been loaded.

        Arguments:
            sermos_yaml (required): String of loaded sermos.yaml file.
    """
    YamlPatternConstructor()  # Add our env variable parser
    try:
        sermos_yaml_schema = SermosYamlSchema()
        # First suss out yaml issues
        sermos_config = yaml.safe_load(sermos_yaml)
        # Then schema issues
        sermos_config = sermos_yaml_schema.load(sermos_config)
    except ValidationError as e:
        msg = "Invalid Sermos configuration due to {}"\
            .format(e.messages)
        logger.error(msg)
        raise InvalidSermosConfig(msg)
    except Exception as e:
        msg = "Invalid Sermos configuration, likely due to invalid "\
            "YAML formatting ..."
        logger.exception("{} {}".format(msg, e))
        raise InvalidSermosConfig(msg)
    return sermos_config


def _get_pkg_name(pkg_name: str) -> str:
    """ Retrieve the normalized package name.
    """
    if pkg_name is None:
        pkg_name = SERMOS_CLIENT_PKG_NAME  # From environment
        if pkg_name is None:
            return None
    return normalized_pkg_name(pkg_name)


def load_sermos_config(pkg_name: str = None,
                       sermos_yaml_filename: str = None,
                       as_dict: bool = True):
    """ Load and parse the `sermos.yaml` file. Issue usable exceptions for
        known error modes so bootstrapping can handle appropriately.

        Arguments:
            pkg_name (required): Directory name for your Python
                package. e.g. my_package_name . If none provided, will check
                environment for `SERMOS_CLIENT_PKG_NAME`. If not found,
                will exit.
            sermos_yaml_filename (optional): Relative path to find your
                `sermos.yaml` configuration file. Defaults to `sermos.yaml`
                which should be found inside your `pkg_name`
            as_dict (optional): If true (default), return the loaded sermos
                configuration as a dictionary. If false, return the loaded
                string value of the yaml file.
    """
    if sermos_yaml_filename is None:
        sermos_yaml_filename = SERMOS_YAML_PATH

    logger.info(f"Loading `sermos.yaml` from package `{pkg_name}` "
                f"and file location `{sermos_yaml_filename}` ...")
    sermos_config = None

    pkg_name = _get_pkg_name(pkg_name)
    if pkg_name is None:  # Nothing to retrieve at this point
        logger.warning("Unable to retrieve sermos.yaml configuration ...")
        return sermos_config

    try:
        sermos_config_path = pkg_resources.resource_filename(
            pkg_name, sermos_yaml_filename)
    except Exception as e:
        msg = "Either pkg_name ({}) or sermos_yaml_filename ({}) is "\
            "invalid ...".format(pkg_name, sermos_yaml_filename)
        logger.error("{} ... {}".format(msg, e))
        raise InvalidPackagePath(e)

    try:
        with open(sermos_config_path, 'r') as f:
            sermos_yaml = f.read()
            sermos_config = parse_config_file(sermos_yaml)
    except InvalidSermosConfig as e:
        raise
    except FileNotFoundError as e:
        msg = "Sermos config file could not be found at path {} ...".format(
            sermos_config_path)
        raise MissingSermosConfig(msg)
    except Exception as e:
        raise e
    if as_dict:
        return sermos_config
    return yaml.safe_dump(sermos_config)


def load_client_config_and_version(pkg_name: str = None,
                                   sermos_yaml_filename: str = None):
    """ Load and parse the `sermos.yaml` file and a client package's version.

        Arguments:
            pkg_name (required): Directory name for your Python
                package. e.g. my_package_name . If none provided, will check
                environment for `SERMOS_CLIENT_PKG_NAME`. If not found,
                will exit.
            sermos_yaml_filename (optional): Relative path to find your
                `sermos.yaml` configuration file. Defaults to `sermos.yaml`
                which should be found inside your `pkg_name`
            as_dict (optional): If true (default), return the loaded sermos
                configuration as a dictionary. If false, return the loaded
                string value of the yaml file.

    For this to work properly, the provided package must be installed in the
    same environment as this Sermos package and it must have a `__version__`
    variable inside its `__init__.py` file, e.g. `__version__ = '0.0.0'`
    """
    sermos_config = None
    client_version = None

    pkg_name = _get_pkg_name(pkg_name)

    try:
        loader = SermosModuleLoader()
        pkg = loader.get_module(pkg_name + '.__init__')
        client_version = getattr(pkg, '__version__', '0.0.0')
        sermos_config = load_sermos_config(pkg_name, sermos_yaml_filename)
    except MissingSermosConfig as e:
        logger.error(e)
    except InvalidSermosConfig as e:
        logger.error(e)
    except InvalidPackagePath as e:
        logger.error(e)
    except Exception as e:
        logger.error("Unable to load client's pkg __version__ or "
                     "{} config file for package: {} ... {}".format(
                         sermos_yaml_filename, pkg_name, e))

    return sermos_config, client_version
