from __future__ import annotations

import abc
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Union

from trainyard.engine import Cluster, LocalCluster


@dataclass
class RemoteObject:
    name: str
    remote_output_ref: Optional[Any] = None  # reference to remote output
    cluster: Optional[Cluster] = None

    def get_result(self) -> Any:
        if self.cluster is None and self.remote_output_ref is None:
            raise ValueError("Remote output or cluster must be specified!")
        if self.remote_output_ref is not None:
            return self.remote_output_ref
        return self.cluster.get(self.name)


# because runhouse needs module level function to be exposed
def _run_task(*args, _task=None, **kwargs):
    return _task(*args, **kwargs)


class TaskWrapper:
    def wrap(self, f: Callable[[Any], Any], task: Task) -> Callable[[Any], Any]:
        return f


class GLOBAL_TASK_WRAPPER:
    task_wrapper: Optional[TaskWrapper] = None

    @staticmethod
    def set_task_wrapper(task_wrapper: TaskWrapper):
        GLOBAL_TASK_WRAPPER.task_wrapper = task_wrapper

    @staticmethod
    def get_task_wrapper():
        return GLOBAL_TASK_WRAPPER.task_wrapper


class Task(metaclass=abc.ABCMeta):
    def __init__(
        self,
        name: str,
        env_requirements: Optional[Union[List[str], str]] = None,
        resources: Optional[Dict[str, Any]] = None,
        config: Dict[str, Any] = {},
        cluster: Cluster = LocalCluster(),
        description: str = "",
    ):
        """
        Base Task object. This is the main runnable function for workflows to run

        Args:
            name (str): name of the task
            env_requirements (Optional[Union[List[str], str]], optional): List of requirements to install on the remote cluster, or path to the requirements.txt file.  Defaults to None.
            resources (Optional[Dict[str, Any]], optional): Optional number (int) of resources needed to run the Function on the Cluster. Keys must be num_cpus and num_gpus.. Defaults to None.
            config (Dict[str, Any], optional): additional config for building the remote function. Defaults to {}.
            cluster (Cluster, optional): cluster to run on. Defaults to LocalCluster().
            description (str): Description for the task.
        """
        self.name = name
        self.env_requirements = env_requirements
        self.resources = resources
        self.config = config
        self.cluster = cluster
        self.description = description
        self.dependencies = []

    def add_dependency(self, dependency: Task) -> None:
        self.dependencies.append(dependency)

    def to(self, cluster: Cluster) -> Task:
        self.cluster = cluster
        return self

    @abc.abstractmethod
    def __call__(self, *args, **kwargs) -> Any:
        """
        Main function for task.
        """

    def remote(self, *args, **kwargs) -> Any:
        _args = []
        for arg in args:
            _arg = arg
            if isinstance(arg, RemoteObject):
                _arg = arg.get_result()
            _args.append(_arg)

        _kwargs = {}
        for kw in kwargs:
            _kwargs[kw] = kwargs[kw]
            if isinstance(kwargs[kw], RemoteObject):
                _kwargs[kw] = kwargs[kw].get_result()

        name, ref = self.cluster.run(
            _run_task,
            name=self.name,
            env_requirements=self.env_requirements,
            resources=self.resources,
            config=self.config,
            _task=self,
            *_args,
            **_kwargs,
        )
        remote_output = RemoteObject(name, ref, self.cluster)
        return remote_output

    def run(self, *args, **kwargs) -> Any:
        """
        Runs the function remotely on `self.cluster`

        Returns:
            RemoteObject: remote output dataclass containing reference to output
        """
        if GLOBAL_TASK_WRAPPER.get_task_wrapper() is None:
            raise ValueError(
                "No GLOBAL_TASK_WRAPPER defined! Tasks must be run within context of a workflow"
            )
        self._wrapped_fn = GLOBAL_TASK_WRAPPER.get_task_wrapper().wrap(
            self.remote, self
        )

        return self._wrapped_fn(*args, **kwargs)


class FunctionTask(Task):
    def __init__(
        self,
        fn: Callable[[Any], Any],
        name: str,
        env_requirements: Optional[Union[List[str], str]] = None,
        resources: Optional[Dict[str, Any]] = None,
        config: Dict[str, Any] = {},
        cluster: Cluster = LocalCluster(),
    ):
        """
        Function Task object. This wraps a fn into a task

        Args:
            fn (Callable[[Any], Any]): callable function to be run
        """
        super().__init__(name, env_requirements, resources, config, cluster)
        self.fn = fn

    def __call__(self, *args, **kwargs) -> Any:
        """
        Runs the fn with args & kwargs

        Returns:
            Any: function output
        """
        return self.fn(*args, **kwargs)


def task(
    fn: Callable[[Any], Any] = None,
    name: str = None,
    env_requirements: Optional[Union[List[str], str]] = None,
    resources: Optional[Dict[str, Any]] = None,
    config: Dict[str, Any] = {},
    cluster: Cluster = LocalCluster(),
):
    """
    Task decorator, returns a Function Task object

    Args:
        fn (Callable[[Any], Any]): callable function to be run
        name (str): name of the function
        env_requirements (Optional[Union[List[str], str]], optional): List of requirements to install on the remote cluster, or path to the requirements.txt file.  Defaults to None.
        resources (Optional[Dict[str, Any]], optional): Optional number (int) of resources needed to run the Function on the Cluster. Keys must be num_cpus and num_gpus.. Defaults to None.
        config (Dict[str, Any], optional): additional config for building the remote function. Defaults to {}.
        cluster (Cluster, optional): cluster to run on. Defaults to LocalCluster().
    """

    def decorator(fn):
        function_name = name
        if function_name is None:
            function_name = fn.__name__
        return FunctionTask(
            fn,
            name=name,
            env_requirements=env_requirements,
            resources=resources,
            config=config,
            cluster=cluster,
        )

    if fn is None:
        return decorator

    function_name = name
    if function_name is None:
        function_name = fn.__name__

    return FunctionTask(
        fn,
        name=function_name,
        env_requirements=env_requirements,
        resources=resources,
        config=config,
        cluster=cluster,
    )


TaskSpec = Union[Task, Callable[[Any], Any]]
