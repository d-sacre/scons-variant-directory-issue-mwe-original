import MWE_Transpiler.Databases.Templates as MWE_Transpiler_Databases_Templates

class Generator:
    def __init__(self):
        pass

    # REMARK: Not intended for usage as a SCons Builder!
    # REMARK: Assumes that build/proceduralFiles/ is the root of the variant
    # directory
    # REMARK: Very simplified, hard coded logic for the MWE to greatly simplify
    # the complex glob based approach in the actual project
    def generate(self) -> dict:
        return {
            "database/values/local/userDefined": [
                {
                    "target": 'databases/local/g_a.values.local.user_defined.json', 
                    "source": 'src/a.values.csv'
                }
            ],
            "database/values/global/userDefined": {
                "target": 'databases/g_a.values.global.user_defined.json',
                "source": ['databases/local/g_a.values.local.user_defined.json']
            },
            "database/calculations/local": [
                {
                    "target": 'databases/local/g_b1.calculation.local.json',
                    "source": ['src/b1.calculations.csv']
                },
                {
                    "target": 'databases/local/g_b2.calculation.local.json',
                    "source": ['src/b2.calculations.csv']
                }
            ],
            "database/calculations/global": {
                "target": 'databases/g_b.calculations.global.json',
                "source": [
                    'databases/local/g_b1.calculation.local.json',
                    'databases/local/g_b2.calculation.local.json'
                ]
            },
            "database/values/global/compiled": {
                "target": 'databases/g_ab.values.global.compiled.json',
                "source": [
                    'databases/g_a.values.global.user_defined.json',
                    'databases/g_b.calculations.global.json'
                ]
            },
            "database/values/local/compiled": [
                {
                    "target": 'databases/local/g_a.values.local.compiled.json',
                    "source": [
                        'databases/local/g_a.values.local.user_defined.json',
                        'databases/local/g_b1.calculation.local.json',
                        'databases/local/g_b2.calculation.local.json',
                        'databases/g_ab.values.global.compiled.json'
                    ]
                }
            ],
            "sourceCode/header/value": [
                {
                    "target": 'src/g_a_values.hpp',
                    "source": [
                        'databases/local/g_a.values.local.compiled.json',
                        'src/transpiler/test_values.transpiler.template.hpp'
                    ]
                }
            ],
            "sourceCode/header/testRoutine": [
                {
                    "target": 'src/g_b1_calculations.hpp',
                    "source": [
                        'databases/local/g_b1.calculation.local.json',
                        'databases/g_ab.values.global.compiled.json',
                        'src/transpiler/test_routine.transpiler.template.hpp'
                    ]
                },
                {
                    "target": 'src/g_b2_calculations.hpp',
                    "source": [
                        'databases/local/g_b2.calculation.local.json',
                        'databases/g_ab.values.global.compiled.json',
                        'src/transpiler/test_routine.transpiler.template.hpp'
                    ]
                }
            ]
        }