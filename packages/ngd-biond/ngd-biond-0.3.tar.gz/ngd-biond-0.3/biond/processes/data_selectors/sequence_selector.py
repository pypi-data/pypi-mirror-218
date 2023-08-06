from biond.processes.data_selectors import DataSelector


class SequenceSelector(DataSelector):

    sequences: {}
    collection: {}
    supermatrix: {}
    filename: {}

    def __init__(self):
        super().__init__("Sequence Selector", "Object in charge of managing the sequences input for the processes")

    def __str__(self):
        return super().__str__() + f"""
        
        Fields:
        sequences: Dictionary with the filter of sequences in the database
        collection: Dictionary with the filter of collection of sequences in the database
        supermatrix: Dictionary with the filter of supermatrices in the database
        filename: Dictionary of file of input containing the keys: path and type (fasta, nexus, etc)
        """

    def get_filter_dict(self):
        pass
