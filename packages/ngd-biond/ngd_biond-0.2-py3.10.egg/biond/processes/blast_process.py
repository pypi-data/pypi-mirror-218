from biond.processes import Process
from biond.processes.data_selectors.sequence_selector import SequenceSelector
from biond.processes.resources.slurm_resource import SlurmResource

from marshmallow import Schema, fields, validate, pre_dump


class BlastProcessSchema(Schema):
    db = fields.Str(validate=validate.OneOf(["nt", "jardin_botanico"]))
    task = fields.Str(validate=validate.OneOf(["blastn", "blastn-short", "megablast", "dc-megablast"]))

    @pre_dump
    def preprocess_dump(self, data):
        data = {'BLAST': data}
        return data


class BlastProcess(Process):

    def __init__(self, db="jardin_botanico", task="megablast"):
        super().__init__("Blast+",
                         "Blast+ finds regions of similarity between biological sequences. The program compares nucleotide sequences to sequence databases and calculates the statistical significance.",
                         [SlurmResource])
        self.db = db
        self.task = task

    def submit(self, data_selectors: [SequenceSelector], resource: SlurmResource) -> str:
        if len(data_selectors) != 1:
            raise ValueError("data_selectors must contain only one SequenceSelector in the BLAST process")
        data = [{
            'selection': data_selectors[0].get_filter_dict(),
            'type': 'fasta',
            'queryParams': '',
            'remote_name': 'query.fasta',
            'object_type': {'bos': 'sequences'}
        }]

        submit_json = {
            'data': data,
            'parameters': {
                'script_params': BlastProcessSchema().dump(self),
                'hpc_params': resource.dump()
            }
        }

        return "JOB_ID"

    def get_details(self) -> str:
        return f"""
        {self.get_details_header()}
        Fields:
        db: Database (nt (genbank), jardin_botanico)
        task: Search program (blastn, blastn-short, megablast, dc-megablast)
        """