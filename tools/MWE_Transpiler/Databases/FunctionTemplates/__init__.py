import MWE_Transpiler.Databases.Templates as MWE_Transpiler_Databases_Templates
import os
import re

# REMARK: Simplified version for MWE, since its functionality is not required
# (function call data base not used during procedural code generation in MWE).
# It is just there to ensure that SCons has as similar dependencies as possible
# compared to the original project
class Generator(
    MWE_Transpiler_Databases_Templates.Base,
    MWE_Transpiler_Databases_Templates.Merging
):
    def __init__(self):
        MWE_Transpiler_Databases_Templates.Base.__init__(self)
        MWE_Transpiler_Databases_Templates.Merging.__init__(self)
        self._keyRegex : str = r'([^\.]{1,})\.function\.call\.transpiler\.template\.cpp'
        self._ending : str = ".function.call.transpiler.template.cpp" 

    def _loadFromCPP(self, a_filePath : str) -> str:
        with open(a_filePath, 'r') as cppFile:
            return cppFile.read()

    def _import(self, a_importFilePaths : list) -> dict:
        _tmp_database : dict = {}

        # DESCRIPTION: Make sure that the processing only starts when the number
        # of specified paths is identical
        for i,_templateFilePath in enumerate(a_importFilePaths):
            _tmp_fileName : str = os.path.basename(str(_templateFilePath))

            # DESCRIPTION: Verify whether file type is correct
            if _tmp_fileName.endswith(self._ending):
                _tmp_key : str = (re.findall(self._keyRegex, _tmp_fileName))[0]

                # DESCRIPTION: Adding the new data to the data base with 
                # rough ID uniqueness verification
                self._addKeyValuePair(
                    _tmp_database,
                    _tmp_key,
                    {
                        "data": self._loadFromCPP(_templateFilePath)
                    }
                )

            else:
                _tmp_message : str = "Invalid file type provided! Expected \"%s\". Aborting!"
                raise Exception(_tmp_message % self._ending)
        
        return _tmp_database

    def generate(self, target, source, env):
        _tmp_database : dict = self._import(source)
        self._export(
            _tmp_database, 
            str(target[0])
        )