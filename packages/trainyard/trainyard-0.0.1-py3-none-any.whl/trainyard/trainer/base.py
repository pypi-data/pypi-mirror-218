# class Trainer(metaclass=abc.ABCMeta):
#     def __init__(self, runner: Runner):
#         self.runner = runner

#     # def create_dataset(self, func, cluster_name: str = "dataset_cluster", cluster_config: Dict[str, Any] = {}, function_config: Dict[str, Any] = {}):
#     #     @wraps(func)
#     #     def wrapped(*args, **kwargs):
#     #         cluster = rh.cluster(name=cluster_name) if rh.exists(cluster_name) else rh.cluster(**cluster_config)
#     #         cluster.up_if_not()
#     #         create_dataset_function = rh.function(func, **function_config)
#     #         return create_dataset_function.remote(*args, **kwargs)
#     #     return wrapped

#     # def process_dataset(self, func, cluster_name: str = "dataset_cluster", cluster_config: Dict[str, Any] = {}, function_config: Dict[str, Any] = {}):
#     #     """
#     #         Decorator that wraps a function that returns a dataset (torch, huggingface, etc)
#     #     """
#     #     @wraps(func)
#     #     def wrapped(dataset, *args, **kwargs):
#     #         cluster = rh.cluster(name=cluster_name) if rh.exists(cluster_name) else rh.cluster(**cluster_config)
#     #         cluster.up_if_not()
#     #         process_dataset_function = rh.function(func, **function_config)
#     #         processed_dataset = process_dataset_function(dataset, *args, **kwargs)
#     #         table = rh.table(data=processed_dataset).write().save(name="dataset", overwrite=True)
#     #         return table
#     #     return wrapped
