import MWE_Transpiler.Databases.Templates as MWE_Transpiler_Databases_Templates

class Generator(MWE_Transpiler_Databases_Templates.FromJSON):
    def __init__(self):
        MWE_Transpiler_Databases_Templates.FromJSON.__init__(self)

    # REMARK: Data stored in global compiled value data base not used in the
    # heavily simplified MWE, but still loaded as source to get the right
    # dependencies for SCons. Reason: The conditions for SCons should be as
    # similar as possible in the MWE
    # REMARK: No dependency based ordering of calculations in data base due
    # to simplification
    def generate(self, target, source, env):
        _tmp_database : dict = {
            "explicit": [],
            "derived": []
        }

        for _source in source:
            _tmp_filePath : str = str(_source)
            _tmp_data : dict = self._loadFromJSON(_tmp_filePath)
            _tmp_categoryID : str = ""

            if _tmp_filePath.endswith('.values.local.user_defined.json'):
                _tmp_categoryID = "explicit"

            if _tmp_filePath.endswith('.calculation.local.json'):
                _tmp_categoryID = "derived"

            if not _tmp_filePath.endswith('.values.global.compiled.json'):
                for _key in _tmp_data:
                    _tmp_entry : dict = _tmp_data[_key]
                    if _tmp_entry not in _tmp_database[_tmp_categoryID]:
                        _tmp_database[_tmp_categoryID].append(_tmp_entry)

        self._export(_tmp_database, str(target[0]))