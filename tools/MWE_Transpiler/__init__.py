from MWE_Transpiler.Databases import Databases as MWE_Transpiler_Databases
from MWE_Transpiler.SourceCode import SourceCode as MWE_Transpiler_SourceCode

class MWE_Transpiler:
    def __init__(self):
        self.Database = MWE_Transpiler_Databases()
        self.SourceCode = MWE_Transpiler_SourceCode()