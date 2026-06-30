from MWE_Transpiler.Databases.FunctionTemplates import Generator as MWE_Transpiler_Databases_FunctionCallTemplates
from MWE_Transpiler.Databases.Values import Values as MWE_Transpiler_Databases_Values
from MWE_Transpiler.Databases.Calculations import Calculations as MWE_Transpiler_Databases_Calculations
from MWE_Transpiler.Databases.TargetSourcePairs import Generator as MWE_Transpiler_Databases_TargetSourcePairs

class Databases:
    def __init__(self):
        self.FunctionCallTemplates = MWE_Transpiler_Databases_FunctionCallTemplates()
        self.Values = MWE_Transpiler_Databases_Values()
        self.Calculations = MWE_Transpiler_Databases_Calculations()
        self.TargetSourcePairs = MWE_Transpiler_Databases_TargetSourcePairs()