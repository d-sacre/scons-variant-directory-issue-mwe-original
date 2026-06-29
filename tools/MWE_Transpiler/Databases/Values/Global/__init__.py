from MWE_Transpiler.Databases.Values.Global.UserDefined import Generator as MWE_Transpiler_Databases_Values_Global_UserDefined
from MWE_Transpiler.Databases.Values.Global.Compiled import Generator as MWE_Transpiler_Databases_Values_Global_Compiled

class Global:
    def __init__(self):
        self.UserDefined = MWE_Transpiler_Databases_Values_Global_UserDefined()
        self.Compiled = MWE_Transpiler_Databases_Values_Global_Compiled()