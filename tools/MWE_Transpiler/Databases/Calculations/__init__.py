from MWE_Transpiler.Databases.Calculations.Local import Generator as MWE_Transpiler_Databases_Calculations_Local
from MWE_Transpiler.Databases.Calculations.Global import Generator as MWE_Transpiler_Databases_Calculations_Global

class Calculations:
    def __init__(self):
        self.Local = MWE_Transpiler_Databases_Calculations_Local()
        self.Global = MWE_Transpiler_Databases_Calculations_Global()