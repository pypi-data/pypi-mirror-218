from biond.processes import Process
from biond.processes.data_selectors.alignment_selector import AlignmentSelector
from biond.processes.resources.ssh_resource import SSHResource

from marshmallow import Schema, fields, validate, pre_dump


class PaupProcessSchema(Schema):
    taxset = fields.List(fields.Str)
    outRoot = fields.Str(validate=validate.OneOf(["politomy", "paraphyletic", "monophyletic"]))
    gapMode = fields.Str(validate=validate.OneOf(["missing", "newState"]))
    method = fields.Str(validate=validate.OneOf(["simple", "bootstrap", "jackknife"]))
    nReplicas = fields.Int(validate=validate.Range(1))
    search = fields.Str(validate=validate.OneOf(["heuristic", "BandB", "fastStep"]))
    le50 = fields.Str(validate=validate.OneOf(["yes", "no"]))
    percent = fields.Int(validate=validate.Range(0, 100))
    addseq = fields.Str(validate=validate.OneOf(["simple", "closest", "asIs", "random", "furthest"]))
    swap = fields.Str(validate=validate.OneOf(["none", "TBR", "SPR", "NNI"]))
    hold = fields.Int(validate=validate.Range(1))

    @pre_dump
    def preprocess_dump(self, data):
        if data['consensus_tree_type'] == "strict":
            data['consensus_tree_type'] = "strict=yes semistrict=no majRule=no adams=no"
        elif data['consensus_tree_type'] == "semistrict":
            data['consensus_tree_type'] = "strict=no semistrict=yes majRule=no adams=no"
        elif data['consensus_tree_type'] == "majority_rule":
            data['consensus_tree_type'] = "strict=no semistrict=no majRule=yes adams=no"
        elif data['consensus_tree_type'] == "adams":
            data['consensus_tree_type'] = "strict=no semistrict=no majRule=no adams=yes"

        data = {'PAUP Parsimony': data}
        return data


class PaupProcess(Process):

    def __init__(self, taxset=[], outRoot="monphyletic", gapMode="newState", method="simple", nReplicas=1,
                 search="heuristic", consensus_tree_type="strict", le50="no", percent=50, addseq="random",
                 swap="TBR", hold=1):
        super().__init__("PAUP",
                         "Phylogenetic analysis using parsimony",
                         [SSHResource])
        self.taxset = taxset
        self.outRoot = outRoot
        self.gapMode = gapMode
        self.method = method
        self.nReplicas = nReplicas
        self.search = search
        self.le50 = le50
        self.percent = percent
        self.addseq = addseq
        self.swap = swap
        self.hold = hold

    def submit(self, data_selectors: [AlignmentSelector], resource: SSHResource) -> str:
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
                'script_params': PaupProcessSchema().dump(self),
            }
        }

        return "JOB_ID"

    def get_details(self) -> str:
        return f"""
        {self.get_details_header()}
        Fields:
        taxset: Set of taxons of the alignment that conform the outgroup
        outRoot: Outgroup Rooting (politomy, paraphyletic, monophyletic)
        gapMode: Gap Mode (missing, newState)
        method: Analysis method (simple, bootstrap, jackknife)
        nReplicas: Number of replicas
        search: Search Strategy (heuristic, BandB, fastStep)
        consensus_tree_type: Consensus Tree Type (strict, semistrict, majority_rule, adams)
        le50: Retain less than 50% of the trees (yes, no)
        percent: Percentage of the trees on which a group must appear in order to be retained
        addseq: Addition Sequence (simple, closest, asIs, random, furthest)
        swap: Branch Swapping (none, TBR, SPR, NNI)
        hold: Number of trees to be held
        """