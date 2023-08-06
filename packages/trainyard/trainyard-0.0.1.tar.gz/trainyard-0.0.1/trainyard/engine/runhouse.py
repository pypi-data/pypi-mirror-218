from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import runhouse as rh

from trainyard.engine.cluster import Cluster


class RunhouseCluster(Cluster):
    def __init__(
        self, name: str = None, instance_type: Optional[str] = None, *args, **kwargs
    ):
        """
        Creates a runhouse cluster with args. For a full list: https://runhouse-docs.readthedocs-hosted.com/en/latest/_modules/runhouse/rns/hardware/cluster_factory.html#cluster

        Args:
            name (str): Name of the cluster
            instance_type (Optional[str], optional): Instance type. This could be a resource (GPU:2) or a type (V100). Defaults to None.
        """
        self.cluster = rh.OnDemandCluster(
            name=name, instance_type=instance_type, *args, **kwargs
        )

    def system(self, commands: List[str], *args, **kwargs):
        """
        Run bash commands on the cluster.
        For more details: https://runhouse-docs.readthedocs-hosted.com/en/latest/api/python/cluster.html

        Args:
            commands (List[str]): commands to run
        """
        self.cluster.run(commands, *args, **kwargs)

    def run(
        self,
        fn: Callable[[Any], Any],
        *args,
        name: Optional[str] = None,
        env_requirements: Optional[Union[List[str], str]] = None,
        resources: Optional[Dict[str, Any]] = None,
        config: Dict[str, Any] = {},
        **kwargs,
    ) -> Tuple[str, Any]:
        """
        Wraps the function in a runhouse.function and automatically attaches it to the runhouse cluster.
        For a full list of Function parameters: https://runhouse-docs.readthedocs-hosted.com/en/latest/api/python/function.html#function-class


        Args:
            fn (Callable[[Any], Any]): Callable function
            name (str): name of the function
            requirements (Optional[Union[List[str], str]], optional): requirements of the function. Defaults to None.
            resources (Optional[Dict[str, Any]], optional): resources of the function. Optional number (int) of resources needed to run the Function on the Cluster. Keys must be num_cpus and num_gpus. Defaults to None.
            config (Dict[str, Any], optional): Additional parameters, see https://runhouse-docs.readthedocs-hosted.com/en/latest/api/python/function.html#function-class. Defaults to {}.

        Returns:
            str: output name
            Any: function output
        """
        self.cluster.up_if_not()
        remote_fn = rh.function(
            fn=fn,
            name=name,
            system=self.cluster,
            env=env_requirements,
            resources=resources,
            **config,
        )
        ref = remote_fn.run(*args, **kwargs)
        return ref.name, ref

    def put(self, key: str, obj: Any, *args, **kwargs) -> str:
        """
        https://runhouse-docs.readthedocs-hosted.com/en/latest/_modules/runhouse/rns/hardware/cluster.html#Cluster.put

        puts object in object store in cluster

        Args:
            key (str): Put the given object on the cluster’s object store at the given key.
            obj (Any): _description_

        Returns:
            str: _description_
        """
        self.cluster.put(key, obj, *args, **kwargs)
        return key

    def get(self, key: str, *args, **kwargs) -> Any:
        """
        https://runhouse-docs.readthedocs-hosted.com/en/latest/_modules/runhouse/rns/hardware/cluster.html#Cluster.get

        Get the result for a given key from the cluster’s object store.

        Args:
            key (str): key to retrieve from runhouse object store

        Returns:
            Any: object in the object store
        """
        return self.cluster.get(key, *args, **kwargs)

    def start(self) -> str:
        self.cluster.up_if_not()
        return self.cluster.address

    def teardown(self) -> None:
        if getattr(self.cluster, "teardown_and_delete", None) is not None:
            self.cluster.teardown_and_delete()

    def save_blob(self, name: str, data: Any, *args, **kwargs) -> str:
        """
        Saves a blob of data into a datastore. For full configuration: https://runhouse-docs.readthedocs-hosted.com/en/latest/api/python/blob.html#blob-factory-method

        Args:
            name (str): name of the blob to save
            data (Any): data to save

        Returns:
            str: name of the blob
        """
        rh.blob(name=name, data=data, *args, **kwargs)
        return name

    def retrieve_blob(self, name: str, *args, **kwargs) -> rh.Blob:
        """
        Retrieves blob of data from datastore.1

        Args:
            name (str): name of blob to retrieve

        Returns:
            rh.Blob: blob object from datastore
        """
        return rh.blob(name=name, *args, **kwargs)
