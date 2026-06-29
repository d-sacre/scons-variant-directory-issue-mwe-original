import MWE_Transpiler.Databases.Templates as MWE_Transpiler_Databases_Templates

class Generator(MWE_Transpiler_Databases_Templates.FromCSV):
    def __init__(self):
        MWE_Transpiler_Databases_Templates.FromCSV.__init__(self)

    def generate(self, target, source, env):
        pass