import MWE_Transpiler.Databases.Templates as MWE_Transpiler_Databases_Templates

class Generator(MWE_Transpiler_Databases_Templates.MergeFromFileJSON):
    def __init__(self):
        MWE_Transpiler_Databases_Templates.MergeFromFileJSON.__init__(self)