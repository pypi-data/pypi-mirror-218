from biond.processes import Process
from biond.processes.data_selectors.geolayer_selector import GeolayerSelector
from biond.processes.data_selectors.phylotree_selector import PhylotreeSelector
from biond.processes.resources.ssh_resource import SSHResource
from typing import Union

from marshmallow import Schema, fields, validate, pre_dump


class PDAProcessSchema(Schema):

    endem = fields.Str(validate=validate.OneOf(["true", "false"]))
    excl = fields.Str(validate=validate.OneOf(["true", "false"]))

    @pre_dump
    def preprocess_dump(self, data):
        data = {'Phylogenetic Diversity Analyzer': data}
        return data


class PDAProcess(Process):

    def __init__(self, endem="false", excl="false"):
        super().__init__("PDA",
                         "Phylogenetic Diversity Analyzer is a software capable of making a quantitative measure to assess the biodiversity of species based on a phylogeny.",
                         [SSHResource])
        self.endem = endem
        self.excl = excl

    def submit(self, data_selectors: [Union[PhylotreeSelector, GeolayerSelector]], resource: SSHResource) -> str:
        if len(data_selectors) != 2 or not any(isinstance(x, PhylotreeSelector) for x in data_selectors) or \
                not any(isinstance(x, GeolayerSelector) for x in data_selectors):
            raise ValueError("data_selectors must contain one PhylotreeSelector and one GeolayerSelector in the PDA "
                             "process")

        phylotree_selector = data_selectors[0]
        geolayer_selector = data_selectors[1]
        if type(phylotree_selector) is GeolayerSelector:
            geolayer_selector = data_selectors[0]
            phylotree_selector = data_selectors[1]

        data = [
            {
                'selection': phylotree_selector.get_filter_dict(),
                'type': 'newick',
                'queryParams': '',
                'remote_name': 'phylotree.newick',
                'object_type': {'bos': 'phylotrees'}
            },
            {
                'selection': geolayer_selector.get_filter_dict(),
                'type': 'nexus',
                'queryParams': '',
                'remote_name': 'area.nexus',
                'object_type': {'geo': 'layers'}
            }
        ]

        submit_json = {
            'data': data,
            'parameters': {
                'script_params': PDAProcessSchema().dump(self)
            }
        }

        return "JOB_ID"

    def get_details(self) -> str:
        return f"""
        {self.get_details_header()}
        Fields:
        endem: Compute endemic PD/SD (true, false)
        excl: Compute exclusive PD/SD (true, false)
        """
