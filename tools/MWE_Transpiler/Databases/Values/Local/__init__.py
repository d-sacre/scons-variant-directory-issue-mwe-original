from MWE_Transpiler.Databases.Values.Local.UserDefined import Generator as MWE_Transpiler_Databases_Values_Local_UserDefined
from MWE_Transpiler.Databases.Values.Local.Compiled import Generator as MWE_Transpiler_Databases_Values_Local_Compiled

class Local:
    def __init__(self):
        self.UserDefined = MWE_Transpiler_Databases_Values_Local_UserDefined()
        self.Compiled = MWE_Transpiler_Databases_Values_Local_Compiled()