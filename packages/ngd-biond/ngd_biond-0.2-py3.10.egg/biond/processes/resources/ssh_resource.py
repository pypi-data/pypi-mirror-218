from biond.processes.resources import Resource, Host


class SSHHost(Host):
    BALDER = "balder"


class SSHResource(Resource):

    def __init__(self, selected_resource: SSHHost, time: float):
        host_list = [e.value for e in SSHHost]
        super().__init__("SSH Resource", "Simple type of resource for using only one CPU", ", ".join(host_list), selected_resource)
        self.time = time

    def __str__(self):
        return super().__str__()
