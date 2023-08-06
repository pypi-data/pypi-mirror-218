import getpass
from trainyard.tasks.tasks import task
from trainyard.engine.runhouse import RunhouseCluster

"""
Setup steps for this. Really annoying but currently the only way to do this without going insane
1. Make sure you can ssh to localhost
2. in one terminal start `ray start --head`
3. in another terminal run `python -m runhouse.servers.http.http_server`
"""

def create_local_cluster():
    print("Creating cluster...")
    cluster = RunhouseCluster(name="local-cluster",ips=['localhost'], ssh_creds={'ssh_user':getpass.getuser(), "ssh_private_key":"~/.ssh/id_rsa.pub"})
    return cluster

def test_run_function():

    cluster = create_local_cluster()

    @task(name="test_function")
    def test_fn(x, y):
        return x**y

    test_fn.to(cluster)

    output = test_fn.run(x=10, y=2)
    assert output.get_result() == 100
