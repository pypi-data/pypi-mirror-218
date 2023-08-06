from abc import ABC
import abc


class DataSelector(ABC):
    name: str
    description: str

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __str__(self):
        return f"""
        Name: {self.name}
        Description: {self.description}
        """

    @abc.abstractmethod
    def get_filter_dict(self):
        raise NotImplementedError
