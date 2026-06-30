import MWE_Transpiler.Databases.Templates as MWE_Transpiler_Databases_Templates

class Generator(MWE_Transpiler_Databases_Templates.FromJSON):
    def __init__(self):
        MWE_Transpiler_Databases_Templates.FromJSON.__init__(self)
        self._filePaths : dict = {}

    def _sortAndValidateSourceFilePaths(self, a_sources : list) -> None:
        for _source in a_sources:
            _tmp_filePath : str = str(_source)

            if _tmp_filePath.endswith(".json"):
                self._filePaths["database/values/local/compiled"] = _tmp_filePath

            if _tmp_filePath.endswith(".hpp"):
                self._filePaths["transpiler/template/header/value"] = _tmp_filePath

    def _createReplacementListsHelper(
        self, a_data : list, a_type : str
    ) -> dict:
        _tmp_data : dict = {
            "declarations": [],
            "assignments": []
        }

        for _entry in a_data[a_type]:
            _tmp_data["declarations"].append(
                "%s %s;" % (_entry["type"], _entry["uuid"])
            )
            _tmp_data["assignments"].append(
                "%s = %s;" % (_entry["uuid"], _entry["operation"])
            )

        return _tmp_data

    # TODO: Add possibility to accept also calculations as values
    def _createReplacementLists(self, a_data : dict) -> dict:
        _tmp_explicit : dict = self._createReplacementListsHelper(
            a_data, "explicit"
        )
        _tmp_derived : dict = self._createReplacementListsHelper(
            a_data, "derived"
        )

        _tmp_replacementLists : dict = {
            "declarations": _tmp_explicit["declarations"] + _tmp_derived["declarations"],
            "assignments": _tmp_explicit["assignments"] + _tmp_derived["assignments"]
        }

        return _tmp_replacementLists

    def _createHeaderData(self, a_replacement : dict) -> str:
        # DESCRIPTION: Read in the hpp template file
        with open(
            self._filePaths["transpiler/template/header/value"], 'r'
        ) as headerTemplateFile:
            _tmp_headerData : str = headerTemplateFile.read()

            # DESCRIPTION: Create the string representations of the declarations
            # and assignments
            _tmp_declarationString : str = ""
            _tmp_assignmentString : str = ""

            # DESCRIPTION: Create the replacement strings
            for j in range(0, len(a_replacement["declarations"])):
                _tmp_declarationString += a_replacement["declarations"][j]
                _tmp_assignmentString += a_replacement["assignments"][j]

                if j != len(a_replacement["declarations"])-1:
                    _tmp_declarationString += "\n"
                    _tmp_assignmentString += "\n"

            # DESCRIPTION: Replace the placeholders in the header data
            _tmp_headerData = _tmp_headerData.replace(
                "<DECLARATIONS>", _tmp_declarationString
            )
            _tmp_headerData = _tmp_headerData.replace(
                "<ASSIGNMENTS>", _tmp_assignmentString
            )

            return _tmp_headerData

    def _export(self, a_data : str, a_filePath : str) -> None:
        with open(a_filePath, 'w') as headerExportFile:
            headerExportFile.write(a_data)

    def generate(self, target, source, env):
        self._sortAndValidateSourceFilePaths(source)

        _tmp_data : dict = self._loadFromJSON(
            self._filePaths["database/values/local/compiled"]
        )
        _tmp_replacementLists : dict = self._createReplacementLists(_tmp_data)
        _tmp_headerData : str = self._createHeaderData(_tmp_replacementLists)
        _tmp_headerData = "// File is procedurally generated!\n\n" + _tmp_headerData

        self._export(_tmp_headerData, str(target[0]))