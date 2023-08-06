from biond.processes.data_selectors import DataSelector


class GeolayerSelector(DataSelector):
    geolayer_id: int

    def __init__(self):
        super().__init__("Phylotree Selector", "Object in charge of managing the geographic layers input for the processes")

    def __str__(self):
        return super().__str__() + f"""

        Fields:
        geolayer_id: ID of the geographic layer
        """

    def get_filter_dict(self):
        pass