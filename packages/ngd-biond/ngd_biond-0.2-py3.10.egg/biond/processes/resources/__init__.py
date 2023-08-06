from abc import ABC
import abc
from enum import Enum


class Host(Enum):
    pass


class Resource(ABC):
    name: str
    description: str
    hosts: []
    selected_host: Host

    def __init__(self, name: str, description: str, hosts: str, selected_host: Host):
        self.name = name
        self.description = description
        self.hosts = hosts

    def __str__(self):
        hosts_str = ", ".join(self.hosts)
        return f"""
        Name: {self.name}
        Description: {self.description}
        Hosts: {hosts_str}
        Selected host: {self.selected_host.value['name']}
        """
