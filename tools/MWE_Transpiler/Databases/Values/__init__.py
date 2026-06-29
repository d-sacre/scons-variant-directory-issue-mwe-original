from MWE_Transpiler.Databases.Values.Local import Local as MWE_Transpiler_Databases_Values_Local
from MWE_Transpiler.Databases.Values.Global import Global as MWE_Transpiler_Databases_Values_Global

class Values:
    def __init__(self):
        self.Local = MWE_Transpiler_Databases_Values_Local()
        self.Global = MWE_Transpiler_Databases_Values_Global()