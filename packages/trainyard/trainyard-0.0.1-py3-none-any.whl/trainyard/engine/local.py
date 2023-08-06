from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from trainyard.engine.cluster import Cluster


class LocalCluster(Cluster):
    def __init__(self, name: str = None, *args, **kwargs):
        self.name = name
        self.object_store: Dict[str, Any] = {}

    def run(
        self,
        fn: Callable[[Any], Any],
        name: Optional[str],
        *args,
        env_requirements: Optional[Union[List[str], str]] = None,
        resources: Optional[Dict[str, Any]] = None,
        config: Dict[str, Any] = {},
        **kwargs,
    ) -> Tuple[str, Any]:
        """
        Runs a remote function with args & kwargs. The cluster object is also passed into the function

        Args:
            fn (Callable[[Any], Any]): callable function
            function_config (Dict[str, Any]): dictionary config for creating the remote function

        Returns:
            Any: name
            Any: function return object(s)
        """
        self.object_store[name] = fn(*args, **kwargs)
        return name, self.object_store[name]

    def put(self, key: str, obj: Any, *args, **kwargs) -> str:
        """
        Put the given object in the local dictionary object store.

        Args:
            key (str): name of object to save
            obj (Any): object to save

        Returns:
            str: name of object
        """
        self.object_store[key] = obj

    def get(self, key: str, *args, **kwargs) -> Any:
        """
        Get the result for a given key from the cluster’s local dictionary object store.

        Args:
            key (str): key of the object to get

        Returns:
            Any: object retrieved from object store
        """
        return self.object_store[key]
