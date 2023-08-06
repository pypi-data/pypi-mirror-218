from __future__ import annotations

import abc
from typing import Any, Callable, Dict, List, Optional, Tuple, Union


class Cluster(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def run(
        self,
        fn: Callable[[Any], Any],
        name: str,
        env_requirements: Optional[Union[List[str], str]] = None,
        resources: Optional[Dict[str, Any]] = None,
        config: Dict[str, Any] = {},
        *args,
        **kwargs,
    ) -> Tuple[str, Any]:
        """
        Run remote function and return a reference if needed!

        Args:
            fn (Callable[[Any], Any]): _description_
            name (str): _description_
            env_requirements (Optional[Union[List[str], str]], optional): _description_. Defaults to None.
            resources (Optional[Dict[str, Any]], optional): _description_. Defaults to None.
            config (Dict[str, Any], optional): _description_. Defaults to {}.

        Returns:
            str: name of the output
            Any: output
        """

    @abc.abstractmethod
    def put(self, key: str, obj: Any, *args, **kwargs) -> str:
        """
        Put the given object on the cluster's object store at the given key.

        Args:
            key (str): name of object to save
            obj (Any): object to save

        Returns:
            str: name of object
        """

    @abc.abstractmethod
    def get(self, key: str, *args, **kwargs) -> Any:
        """
        Get the result for a given key from the cluster's object store.

        Args:
            key (str): key of the object to get

        Returns:
            Any: object retrieved from object store
        """

    def start(self) -> str:
        """
        Starts the clster

        Returns:
            str: address of cluster
        """
        return "local"

    def teardown(self) -> None:
        """
        Teardown and delete the cluster
        """
        pass

    def save_blob(self, name: str, data: Any, *args, **kwargs) -> str:
        """
        Saves blob to the cluster with associated name. By default just calls put

        Args:
            name (str): Name of object to save
            data (Any): content to save

        Returns:
            str: name of content
        """
        return self.put(key=name, obj=data, *args, **kwargs)

    def retrieve_blob(self, name: str, *args, **kwargs) -> Any:
        """
        Retrieves a blob from the cluster with associated name. By default just calls get

        Args:
            name (str): name of object to retrieve

        Returns:
            Any: Retrieved type can be anything. This may be a ref to the object itself
        """
        return self.get(key=name, *args, **kwargs)
