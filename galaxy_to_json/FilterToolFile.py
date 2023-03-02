import json
from galaxy_to_json import ReadInput
from galaxy_to_json.tools import StaramrFilter, PlasmidFinderFilter

class FilterToolfile(ReadInput):

    def __init__(self):
        super().__init__()

    def _check_different_colnames(self, file_colname, template_colname):
        colname_differences = set(file_colname) ^ set(template_colname)



