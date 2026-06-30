import MWE_Transpiler.Databases.Templates as MWE_Transpiler_Databases_Templates
import MWE_Utilities as mweu

class Generator(MWE_Transpiler_Databases_Templates.FromJSON):
    def __init__(self):
        MWE_Transpiler_Databases_Templates.FromJSON.__init__(self)
        self._filePaths : dict = {}

    def _sortAndValidateSourceFilePaths(self, a_sources : list) -> None:
        for _source in a_sources:
            _tmp_filePath : str = str(_source)

            if _tmp_filePath.endswith(".calculations.local.json"):
                self._filePaths["database/calculations/local"] = _tmp_filePath

            if _tmp_filePath.endswith(".hpp"):
                self._filePaths["transpiler/template/header/testRoutine"] = _tmp_filePath

    def _createHeaderData(self, a_calculations : dict) -> str:
        # DESCRIPTION: Read in the hpp template file
        with open(
            self._filePaths["transpiler/template/header/testRoutine"], 'r'
        ) as headerTemplateFile:
            _tmp_headerData : str = headerTemplateFile.read()

            # DESCRIPTION: Generate the test routine ID from the file name
            _tmp_testRoutineID : str = (((mweu.Path.Manipulation.getTail(
                self._filePaths["database/calculations/local"]
            )).split("."))[0]).replace("g_", "").capitalize()
            
            # DESCRIPTION: Create all the calculation "calls"
            _tmp_functionCalls : str = ""

            for _key in a_calculations:
                _tmp_data : dict = a_calculations[_key]

                _tmp_replacement : tuple = (
                    _tmp_data["uuid"], 
                    _tmp_data["operation"],
                    "m_values->%s" % _tmp_data["uuid"]
                )
                _tmp_functionCalls += "std::cout << \"UUID %s: %s = \" << %s <<" % _tmp_replacement
                _tmp_functionCalls += r' "\n";'
                _tmp_functionCalls += "\n"

            # DESCRIPTION: Replace test routine ID place holders
            _tmp_headerData = _tmp_headerData.replace(
                "<TEST_ROUTINE_ID>", _tmp_testRoutineID
            )

            _tmp_headerData = _tmp_headerData.replace(
                "<RUN>", _tmp_functionCalls
            )

            return _tmp_headerData

    def _export(self, a_data : str, a_filePath : str) -> None:
        with open(a_filePath, 'w') as headerExportFile:
            headerExportFile.write(a_data)

    # REMARK: Global compiled value data base not used in simplified MWE, just 
    # passed in so that SCons sees the identical dependencies like in the real
    # project
    def generate(self, target, source, env):
        self._sortAndValidateSourceFilePaths(source)
        _tmp_calculations : dict = self._loadFromJSON(
            self._filePaths["database/calculations/local"]
        )
        _tmp_headerData : str = self._createHeaderData(_tmp_calculations)
        self._export(_tmp_headerData, str(target[0]))