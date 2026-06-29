from MWE_Transpiler.SourceCode.Header.Values import Generator as MWE_Transpiler_SourceCode_Header_Values
from MWE_Transpiler.SourceCode.Header.TestRoutines import Generator as MWE_Transpiler_SourceCode_Header_TestRoutines

class Header:
    def __init__(self):
        self.Values = MWE_Transpiler_SourceCode_Header_Values()
        self.TestRoutines = MWE_Transpiler_SourceCode_Header_TestRoutines()