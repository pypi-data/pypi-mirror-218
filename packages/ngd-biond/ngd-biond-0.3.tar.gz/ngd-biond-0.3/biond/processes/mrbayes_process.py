from biond.processes import Process
from biond.processes.data_selectors.sequence_selector import SequenceSelector
from biond.processes.resources.cipres_resource import CipresResource
from biond.processes.resources.slurm_resource import SlurmResource

from marshmallow import Schema, fields, validate, pre_dump


class MrBayesProcessSchema(Schema):
    taxons_select = fields.List(fields.Str)
    nst = fields.Str(validate=validate.OneOf(["1", "2", "6", "mixed"]))
    rates = fields.Str(validate=validate.OneOf(["equal", "gamma", "lnorm", "adgamma", "propinv", "invgamma", "kmixture"]))
    ngen = fields.Int(validate=validate.Range(1))
    nchains = fields.Int(validate=validate.Range(1))
    samplefreq = fields.Int(validate=validate.Range(1))
    burninfrac = fields.Int(validate=validate.Range(0, 1))

    @pre_dump
    def preprocess_dump(self, data):
        data = {'Mr Bayes': data}
        return data


class MrBayesProcess(Process):

    def __init__(self, taxons_select=[], nst="6", rates="invgamma", ngen=1000000, nchains=4, samplefreq=500, burninfrac=0.25):
        super().__init__("Mr Bayes",
                         "MrBayes is a program for Bayesian inference and model choice across a wide range of phylogenetic and evolutionary models.",
                         [SlurmResource, CipresResource])
        self.taxons_select = taxons_select
        self.nst = nst
        self.rates = rates
        self.ngen = ngen
        self.nchains = nchains
        self.samplefreq = samplefreq
        self.burninfrac = burninfrac

    def submit(self, data_selectors: [SequenceSelector], resource: SlurmResource or CipresResource) -> str:
        if len(data_selectors) != 1:
            raise ValueError("data_selectors must contain only one AlignmentSelector in the PAUP process")
        data = [{
            'selection': data_selectors[0].get_filter_dict(),
            'type': 'nexus',
            "queryParams": "?header=\"organism_canon_underscored\"",
            'remote_name': 'aln.nexus',
            'object_type': {'bos': 'alignments'}
        }]

        submit_json = {
            'data': data,
            'parameters': {
                'script_params': MrBayesProcessSchema().dump(self)
            }
        }

        if type(resource) is SlurmResource:
            submit_json['parameters']['hpc_params'] = resource.dump()

        return "JOB_ID"

    def get_details(self) -> str:
        return f"""
        {self.get_details_header()}
        Fields:
        taxons_select: Set of taxons of the alignment that conform the outgroup
        nst: Number of substitution types (1, 2, 6, mixed)
        rates: Among-site rate variation model (equal, gamma, lnorm, adgamma, propinv, invgamma, kmixture)
        ngen: Number of generations
        nchains: Number of chains
        samplefreq: Sample frequency
        burninfrac: Burnin Fraction
        """
