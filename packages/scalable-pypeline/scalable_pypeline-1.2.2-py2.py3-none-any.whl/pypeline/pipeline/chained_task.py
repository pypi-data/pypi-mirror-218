import logging
from celery import Task
from pypeline.utils.task_utils import PipelineRunWrapper


logger = logging.getLogger(__name__)


class ChainedTask(Task):
    """ A Celery Task that is used as the _base_ for all dynamically
    generated tasks (by GenerateCeleryTasks().generate()). This injects
    `event` into every task's signature, which allows pipelines to pass
    event information easily through a chain.
    """
    abstract = True

    def __call__(self, *args, **kwargs):
        """ Allow the return value of one task to update the kwargs of a
            subsequent task if it's a dictionary. Important to the function
            of a pipeline to allow event information to flow easily.
        """
        # Inject app context
        if len(args) == 1 and isinstance(args[0], dict):
            kwargs.update(args[0])
            args = ()

        # Event holds information used in PipelineRunWrapper and
        # other areas.
        if 'event' not in kwargs.keys():
            kwargs['event'] = {}
        # This is a special worker from dyrygent that orchestrates our
        # pipelines.  It provides a patch in fix for celery's poor
        # implementation of Canvas work-flows
        if self.__name__ == 'workflow_processor':
            kwargs.pop('event', None)
        return super(ChainedTask, self).__call__(*args, **kwargs)

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        if "event" in kwargs and "pipeline_id" in kwargs["event"]:
            try:
                pipeline_run_wrapper: PipelineRunWrapper = \
                    PipelineRunWrapper.from_event(kwargs["event"])
                current_task_status = pipeline_run_wrapper.get_task_celery_status(task_id)
            except Exception:
                logger.exception("Unable to retreive Pipeline Run Wrapper")
                return

            if current_task_status:
                current_task_status["status"] = status
            try:
                pipeline_run_wrapper.save_to_cache()
            except Exception:
                logger.exception(f"Failed to update celery task status for task {task_id}")

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        if "event" in kwargs and "pipeline_id" in kwargs["event"]:
            try:
                pipeline_run_wrapper: PipelineRunWrapper = \
                    PipelineRunWrapper.from_event(kwargs["event"])
                current_task_status = pipeline_run_wrapper.get_task_celery_status(task_id)
            except Exception:
                logger.exception("Unable to retreive Pipeline Run Wrapper")
                return

            if current_task_status:
                current_task_status["retries"] = current_task_status["retries"] + 1
            try:
                pipeline_run_wrapper.save_to_cache()
            except Exception:
                logger.exception(f"Failed to update celery task status for task {task_id}")
