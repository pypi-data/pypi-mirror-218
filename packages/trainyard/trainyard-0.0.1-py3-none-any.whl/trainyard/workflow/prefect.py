from typing import Any, Callable, Dict

import prefect

from trainyard.tasks.tasks import Task, TaskWrapper
from trainyard.workflow.workflow import WorkflowBackend


class PrefectTaskWrapper(TaskWrapper):
    def wrap(self, f: Callable[[Any], Any], task: Task) -> Callable[[Any], Any]:
        return prefect.task(
            name=task.name,
            description=task.description,
            # task_run_name="{name}-on-{date:%A}",
        )(f)


class PrefectWorkflowBackend(WorkflowBackend):
    def __init__(self, workflow_params: Dict[str, Any] = {}):
        self.workflow_params = workflow_params

    def setup_task_wrapper(self):
        return PrefectTaskWrapper()

    def create_workflow(
        self, name: str, workflow_function: Callable[[Any], Any]
    ) -> prefect.Flow:
        return prefect.flow(name=name, **self.workflow_params)(workflow_function)
