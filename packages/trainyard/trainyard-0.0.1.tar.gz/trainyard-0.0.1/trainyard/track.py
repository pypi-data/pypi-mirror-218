import abc
from typing import Any

from trainyard.workflow.prefect import PrefectWorkflowBackend
from trainyard.workflow.workflow import WorkflowBackend


class Track(metaclass=abc.ABCMeta):
    @property
    def name(self) -> str:
        return self.__class__.__name__

    @abc.abstractmethod
    def __call__(self, *args, **kwargs):
        """
        Main method for creating tracks. Populate this with as many tasks as you want
        """

    def run(
        self,
        *args,
        workflow_backend: WorkflowBackend = PrefectWorkflowBackend(),
        **kwargs,
    ) -> Any:
        with workflow_backend as wf_context:
            wf = wf_context.create_workflow(
                name=self.name, workflow_function=self.__call__
            )
            return wf(*args, **kwargs)
