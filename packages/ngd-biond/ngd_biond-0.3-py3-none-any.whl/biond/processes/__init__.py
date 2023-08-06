from abc import ABC
import abc


class Process(ABC):
    name: str
    description: str
    resources: []

    def __init__(self, name, description, resources):
        self.name = name
        self.description = description
        self.resources = resources

    def get_details_header(self) -> str:
        resources_str = ", ".join(self.resources.name)
        return f"""
        Name: {self.name}
        Description: {self.description}
        Resources: {resources_str}
        """

    def has_resource(self, resource: str) -> bool:
        return resource in self.resources

    @abc.abstractmethod
    def get_details(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def submit(self, data_selectors, resource) -> str:
        raise NotImplementedError

    def help(self):
        print(self.get_details())
