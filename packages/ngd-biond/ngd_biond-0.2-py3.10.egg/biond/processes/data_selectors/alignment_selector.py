from biond.processes.data_selectors import DataSelector


class AlignmentSelector(DataSelector):
    alignments: {}
    filename: {}

    def __init__(self):
        super().__init__("Alignment Selector", "Object in charge of managing the alignments input for the processes")

    def __str__(self):
        return super().__str__() + f"""

        Fields:
        alignments: Dictionary with the filter of alignments in the database
        filename: Dictionary of file of input containing the keys: path and type (fasta, nexus, etc)
        """

    def get_filter_dict(self):
        pass