from __future__ import annotations

import abc
from typing import Any, Callable

from trainyard.tasks.tasks import GLOBAL_TASK_WRAPPER, TaskWrapper  # noqa


class WorkflowBackend(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def setup_task_wrapper(self) -> TaskWrapper:
        """
        Overrides GLOBAL_TASK_WRAPPER so that tasks can be executed with the task
        """

    def __enter__(self) -> WorkflowBackend:
        """
        Overrides GLOBAL_TASK_WRAPPER so that tasks can be executed with the task
        """
        GLOBAL_TASK_WRAPPER.set_task_wrapper(self.setup_task_wrapper())
        return self

    def shutdown_task_wrapper(self):
        """
        Tears down workflow backend
        """
        pass

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Resets GLOBAL_TASK_WRAPPER

        Args:
            exc_type (_type_): _description_
            exc_val (_type_): _description_
            exc_tb (_type_): _description_
        """
        self.shutdown_task_wrapper()
        GLOBAL_TASK_WRAPPER.set_task_wrapper(None)

    @abc.abstractmethod
    def create_workflow(
        self, name: str, workflow_function: Callable[[Any], Any]
    ) -> Callable[[Any], Any]:
        """
        Creates a workflow using a workflow function that contains tasks

        Args:
            name (str): The name of the workflow
            workflow_function (Callable[[Any], Any]): workflow_function
        """
