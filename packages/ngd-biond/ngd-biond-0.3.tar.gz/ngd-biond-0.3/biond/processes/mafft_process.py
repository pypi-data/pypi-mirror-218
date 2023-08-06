from biond.processes import Process
from biond.processes.data_selectors.sequence_selector import SequenceSelector
from biond.processes.resources.cipres_resource import CipresResource
from biond.processes.resources.slurm_resource import SlurmResource

from marshmallow import Schema, fields, validate, pre_dump


class MafftProcessSchema(Schema):

    algorithm = fields.Str(validate=validate.OneOf(["6merpair", "globalpair", "localpair", "genafpair", "fastapair"]))
    retree = fields.Int(validate=validate.Range(1))
    parttree = fields.Str(validate=validate.OneOf(["none", "parttree", "dpparttree"]))
    maxiterate = fields.Int(validate=validate.Range(0))

    @pre_dump
    def preprocess_dump(self, data):
        data['algorithm'] = f"--{data['algorithm']}"
        data['parttree'] = "" if data['parttree'] == "none" else f"--{data['parttree']}"
        data = {'MAFFT': data}
        return data

class MAFFTProcess(Process):

    def __init__(self, algorithm="globalpair", retree=2, parttree="dpparttree", maxiterate=0):
        super().__init__("MAFFT",
                         "MAFFT (Multiple Alignment using Fast Fourier Transform) is a high speed multiple sequence alignment program.",
                         [SlurmResource, CipresResource])
        self.algorithm = algorithm
        self.retree = retree
        self.parttree = parttree
        self.maxiterate = maxiterate

    def submit(self, data_selectors: [SequenceSelector], resource: SlurmResource or CipresResource) -> str:
        if len(data_selectors) != 1:
            raise ValueError("data_selectors must contain only one SequenceSelector in the MAFFT process")
        data = [{
            'selection': data_selectors[0].get_filter_dict(),
            'type': 'fasta',
            'queryParams': '',
            'remote_name': 'input.fasta',
            'object_type': {'bos': 'sequences'}
        }]

        submit_json = {
            'data': data,
            'parameters': {
                'script_params': MafftProcessSchema().dump(self)
            }
        }

        if type(resource) is SlurmResource:
            submit_json['parameters']['hpc_params'] = resource.dump()

        return "JOB_ID"

    def get_details(self) -> str:
        return f"""
        {self.get_details_header()}
        Fields:
        algorithm: Alignment algorithm (6merpair, globalpair, localpair, genafpair, fastapair)
        retree: Repeat Guide Tree retree times. Only available if algorithm = 6merpair
        parttree: Type of PartTree algorithm (none, parttree, dpparttree). Only available if algorithm = 6merpair
        maxiterate: Maximum Iterations (0: no limit)
        """
