import random
import string
from typing import Optional

from trainyard.engine.cluster import Cluster
from trainyard.engine.local import LocalCluster
from trainyard.engine.runhouse import RunhouseCluster

CLUSTER_MAP = {"local": LocalCluster, "runhouse": RunhouseCluster}


def cluster(
    backend: str = "runhouse",
    name: Optional[str] = None,
    instance_type: Optional[str] = None,
    *args,
    **kwargs,
):
    if name is None:
        name = "".join(random.choice(string.lowercase) for x in range(10))
        name = f"cluster_{name}"
    cluster_class = CLUSTER_MAP.get(backend, RunhouseCluster)
    return cluster_class(name, instance_type, *args, **kwargs)


__all__ = ["Cluster", "LocalCluster", "RunhouseCluster", "cluster"]
