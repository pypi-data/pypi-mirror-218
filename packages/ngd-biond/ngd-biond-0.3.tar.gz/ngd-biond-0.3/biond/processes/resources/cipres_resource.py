from biond.processes.resources import Resource, Host


class CipresHost(Host):
    SDSC = "San Diego Supercomputer Center"


class CipresResource(Resource):

    def __init__(self, time: float):
        host_list = [e.value["name"] for e in CipresHost]
        super().__init__("Cipres Resource", "Resource for using the San Diego Supercomputer Center. It doesn't allow "
                                            "to select how much cpu or gpu to use, so the time is the only parameter "
                                            "of this resource.", ", ".join(host_list), CipresHost.SDSC)
        self.time = time

    def __str__(self):
        return super().__str__() + f"\n Time: {self.time}"
