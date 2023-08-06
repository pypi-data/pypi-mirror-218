from biond.processes import Process
from biond.processes.data_selectors.sequence_selector import SequenceSelector
from biond.processes.resources.ssh_resource import SSHResource

from marshmallow import Schema, fields, validate, pre_dump


class ClustalProcessSchema(Schema):
    dnarna = fields.Str(validate=validate.Equal("DNA"))
    outform = fields.Str(validate=validate.OneOf(["fasta", "clustal", "phylip"]))
    out_seqnos = fields.Str(validate=validate.OneOf(["ON", "OFF"]))
    out_order = fields.Str(validate=validate.OneOf(["ALIGNED", "INPUT"]))
    mode = fields.Str(validate=validate.OneOf(["complete", "part"]))
    seq_range_start = fields.Int(validate=validate.Range(1))
    seq_range_end = fields.Int(validate=validate.Range(1))#TODO: max?

    @pre_dump
    def preprocess_dump(self, data):
        data = {'MSA ClustalW': data}
        return data


class ClustalProcess(Process):

    def __init__(self, outform="fasta",
                 out_order="ALIGNED", mode="complete", seq_range_start=1, seq_range_end=99999, out_seqnos="OFF", ):
        super().__init__("ClustalW",
                         "ClustalW is a general purpose multiple sequence alignment program for DNA",
                         [SSHResource])
        if seq_range_start >= seq_range_end:
            raise ValueError("seq_range_start should be strictly lower than seq_range_end")
        self.dnarna = "DNA"
        self.outform = outform
        self.out_order = out_order
        self.mode = mode
        self.seq_range_start = seq_range_start
        self.seq_range_end = seq_range_end
        self.out_seqnos = out_seqnos

    def submit(self, data_selectors: [SequenceSelector], resource: SSHResource) -> str:
        if len(data_selectors) != 1:
            raise ValueError("data_selectors must contain only one SequenceSelector in the ClustalW process")
        data = [{
            'selection': data_selectors[0].get_filter_dict(),
            'type': 'fasta',
            'queryParams': '',
            'remote_name': 'input_dataset.fasta',
            'object_type': {'bos': 'sequences'}
        }]

        submit_json = {
            'data': data,
            'parameters': {
                'script_params': ClustalProcessSchema().dump(self),
            }
        }

        return "JOB_ID"

    def get_details(self) -> str:
        return f"""
        {self.get_details_header()}
        Fields:
        outform: Output alignment format (fasta, clustal, phylip)
        out_seqnos: Show residue numbers in clustal format output. Only available when outform = clustal (ON, OFF)
        out_order: Output order (ALIGNED, INPUT)
        mode: Output complete alignment or specify part to output (complete, part)
        seq_range_start: Start point of part to output. Only available whe mode = part
        seq_range_end: End point of part to output. Only available whe mode = part
        """
