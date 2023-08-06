from marshmallow import Schema, fields, validate, pre_dump

from biond.processes.resources import Resource, Host


class SlurmHost(Host):
    BALDER = {
        "name": "balder",
        "n_nodes": 1,
        "n_cpus_per_node": 64,
        "n_gpus_per_node": 3
    }
    TEIDE = {
        "name": "Teide HPC",
        "n_nodes": 1028,
        "n_cpus_per_node": 16,
        "n_gpus_per_node": 0
    }


class TeideSchema(Schema):
    nodes: fields.Int(validate=validate.Range(0, SlurmHost.TEIDE.value['n_nodes']))
    cpus_per_node: fields.Int(validate=validate.Range(0, SlurmHost.TEIDE.value['n_cpus_per_node']))
    gpus_per_node: fields.Int(validate=validate.Range(0, SlurmHost.TEIDE.value['n_gpus_per_node']))
    time: fields.Float(validate=validate.Range(0.5))

    @pre_dump
    def pre_dump_teide(self, data):
        keys_dict = {'nodes': 'ntasks', 'cpus_per_node': 'cpus_per_task', 'gpus_per_node': 'gpus'}
        for old_key, new_key in keys_dict.items():
            data[new_key] = data[old_key]
            del data[old_key]
        return data



class BalderSchema(Schema):
    nodes: fields.Int(validate=validate.Range(0, SlurmHost.BALDER.value['n_nodes']))
    cpus_per_node: fields.Int(validate=validate.Range(0, SlurmHost.BALDER.value['n_cpus_per_node']))
    gpus_per_node: fields.Int(validate=validate.Range(0, SlurmHost.BALDER.value['n_gpus_per_node']))
    time: fields.Float(validate=validate.Range(0.5))

    @pre_dump
    def pre_dump_balder(self, data):
        keys_dict = {'nodes': 'ntasks', 'cpus_per_node': 'cpus_per_task', 'gpus_per_node': 'gpus'}
        for old_key, new_key in keys_dict.items():
            data[new_key] = data[old_key]
            del data[old_key]
        return data


class SlurmResource(Resource):

    def __init__(self, selected_host: SlurmHost, cpus_per_node: int, gpus_per_node: int, time: float, nodes=1):
        host_list = [e.value["name"] for e in SlurmHost]
        super().__init__("Slurm Resource",
                         "This type of resource is used for processes with heavy demand of resources. It enables to configure the quantity of time, cpus or gpus to use. ",
                         ", ".join(host_list), selected_host)

        if cpus_per_node < 1 and gpus_per_node < 1:
            raise ValueError(f"At least gpus_per_node or gpus should be greater than 0")

        self.cpus_per_node = cpus_per_node
        self.gpus_per_node = gpus_per_node
        self.nodes = nodes
        self.time = time
        self.selected_host = selected_host

    def __str__(self):
        return super().__str__() + f"""
        N. of nodes: {self.selected_host.value["n_nodes"]}
        N. of cpus per node: {self.selected_host.value["n_cpus_per_node"]}
        N. of gpus per node: {self.selected_host.value["n_gpus_per_node"]}
        CPUs to use: {self.cpus_per_node}
        GPUs to use: {self.gpus_per_node}
        Time in hours: {self.time}
        """

    def dump(self):
        if self.selected_host == SlurmHost.TEIDE:
            return TeideSchema().dump(self)
        elif self.selected_host == SlurmHost.BALDER:
            return BalderSchema().dump(self)
