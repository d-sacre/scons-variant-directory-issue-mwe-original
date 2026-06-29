import MWE_Transpiler.Databases.Templates as MWE_Transpiler_Databases_Templates

class Generator(MWE_Transpiler_Databases_Templates.FromCSV):
    def __init__(self):
        MWE_Transpiler_Databases_Templates.FromCSV.__init__(self)

    def _processSingleLine(self, a_header : list, a_lineData : str) -> dict:
        _tmp_data : dict = super()._processSingleLine(a_header, a_lineData)
        _tmp_data["operation_type"] = "value"

        return _tmp_data