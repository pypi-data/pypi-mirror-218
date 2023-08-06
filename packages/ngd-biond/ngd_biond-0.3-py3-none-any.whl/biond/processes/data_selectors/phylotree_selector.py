from biond.processes.data_selectors import DataSelector


class PhylotreeSelector(DataSelector):
    phylotrees: {}
    filename: {}

    def __init__(self):
        super().__init__("Phylotree Selector", "Object in charge of managing the phylogenetic trees input for the processes")

    def __str__(self):
        return super().__str__() + f"""

        Fields:
        phylotrees: Dictionary with the filter of phylotrees in the database
        filename: Dictionary of file of input containing the keys: path and type (newick, nexus, etc)
        """

    def get_filter_dict(self):
        pass
