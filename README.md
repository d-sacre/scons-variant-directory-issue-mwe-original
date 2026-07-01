# SCons Variant Directory Shenanigans
A minimal not working example of SCons Variant Directory shenanigans. Just as a reference on what not to do for [my question on Stack Overflow.](https://stackoverflow.com/questions/79966509/how-to-prevent-scons-from-deleting-everything-in-variant-directories-before-buil)  

# IMPORTANT: BAD PRACTICE
NOT SUITABLE FOR RE-USAGE IN ANY FORM, ESPECIALLY NOT IN PRODUCTION.
THE SOFTWARE IS PROVIDED AS IS. THE AUTHOR REFUSES ANY LIABILITY. 

# How to run
## Requirements
- Linux x86_64 or Windows amd64 as operating system (others currently not implemented)
- SCons 4.10.1 and Python > 3.10 available
- A C++ compiler (any that supports C++20 should do and be automatically detected)

## Command
To start the compilation, run the following command:
```
scons --target-platform=<YOUR_HOST_PLATFORM>
```
Available options are: `linux.x86_64`, `windows.amd64`.<br>
If you specify a target platform that is different to your host platform, the build tool
will halt with an error (cross-compilation is not implemented in this MWE).

# Problem
The implementation described above was working for several weeks without any issues. 
Suddenly, SCons started to build the procedural files for each run, even though there were no changes which would have required a rebuild. 
Upon further inspection, it seems that SCons now deletes every procedural file before starting the build process for no reason. 
At the moment, the produced files are still valid, so in theory, the constant rebuilding is just a nuisance; 
it makes debugging and implementing new features more difficult. However, I had a similar issue in the past, which I ignored until one 
day SCons could no longer build the files. <br>
**REMARK:** This version of the MWE does **NOT** show the constant deletion in the variant directory `build/proceduralFiles`. It is only the starting point for further investigations.

# Background
I am currently working on a transpiler to convert test requirements (stored as `.csv`) to compilable C++ code (both `.hpp` and in the future also `.cpp`).

## Project structure
To keep the project manageable, the SCons build routine is separated into several variant directories:
- one variant directory for the data generated during the transpilation (`.json`, `.hpp`, `.cpp`)
- one variant directory for each supported target platform, where the binaries will be created
The source code files which are generated during transpilation are copied to the `src/` directory before the compilation starts.<br>
The project structure after successful compilation looks like this (procedurally generated files are prefixed with `g_`):
```
<ROOT>
  ├── SConstruct
  ├── src
  │    ├── transpiler
  │    │       └── <TEMPLATES>
  │    ├── a.values.csv
  │    ├── b1.calculations.csv
  │    ├── b2.calculations.csv
  │    ├── g_a_values.hpp
  │    ├── g_b1_calculations.hpp
  │    ├── g_b2_calculations.hpp
  │    └── test.cpp  
  └── build
        ├── proceduralFiles
        │         ├── SConscript
        │         ├── databases
        │         │       ├── local
        │         │       │     ├── g_a.values.local.compiled.json
        │         │       │     ├── g_a.values.local.user_defined.json
        │         │       │     ├── g_b1.calculations.local.json
        │         │       │     └── g_b2.calculations.local.json
        │         │       ├── g_a.values.global.user_defined.json
        │         │       ├── g_b.calculations.global.json
        │         │       ├── g_ab.values.global.compiled.json
        │         │       └── g_test.function.call.template.database.json
        │         └── src
        │              ├── g_a_values.hpp
        │              ├── g_b1_calculations.hpp
        │              └── g_b2_calculations.hpp
        └── executables
                  ├── SConscript
                  ├── windows
                  │      ├── SConscript
                  │      ├── bin
                  │      │    └── test.exe
                  │      └── src
                  │           └── <OBJECT_FILES>
                  └── linux
                         ├── SConscript
                         ├── bin
                         │    └── test.x86_64
                         └── src
                              └── <OBJECT_FILES>
```
## SCons Setup
To achieve the desired variant directory setup, all `SConscript` files (except `build/executables/SConscript`) follow this concept:
```python
Import('env') # REMARK: Defined in SConstruct and exported

VariantDir('./', '<BACK_TO_ROOT>', duplicate = False)
<LOCAL_ENV> = env.Clone()
```
The source directory path is set for each `SConscript` file in such a way, that the variant source directory is identical with the project root directory. For example, fo `build/proceduralFiles/SConscript`, this will look like this:
```python
Import('env') # REMARK: Defined in SConstruct and exported

VariantDir('./', '../../', duplicate = False)
proceduralFiles = env.Clone()
```
I resorted to using the `VariantDir()` function instead of specifing the variant directory when loading the `SConscript` file
```python
SConscript(<FILE_PATH>, variant_dir = <DIRECTORY>)
```
since I could not get the latter approach to work correctly.

## Transpiler Implementation
The transpiler is implemented in the following way:
1. Parse `src/*.csv` to `build/proceduralFiles/databases/local/g_*.local.json`.
2. From `<DATABASE_ROOT>/local/g_*.local(.user_defined).json` create the global variants <br>`<DATABASE_ROOT>/g_*.global(.user_defined).json`.
3. Combine `<DATABASE_ROOT>/g_a.values.global.user_defined.json` with `<DATABASE_ROOT>/g_b.global.json` to create `<DATABASE_ROOT>/g_ab_values.global.compiled.json`.
4. Create `build/proceduralFiles/src/g_a_values.hpp` from `<DATABASE_ROOT>/g_ab.values.global.json` and the corresponding transpiler template.
5. Create `build/proceduralFiles/src/g_b*_calculations.hpp` from `<DATABASE_ROOT>/g_ab_values.global.json`, `<DATABASE_ROOT>/local/g_b*_values.global.json`, `<DATABASE_ROOT>/g_test.function.call.template.database.json` and the corresponding transpiler template.
6. Use the SCons Copy factory to copy all the source files from `build/proceduralFiles/src/*` to `src/*`.

Some static configuration/code template files used for step 4 and step 5 have been omitted, since they are not relevant for the problem.<br>
In summary, a combination of static and procedural files are used to create (other) procedural files.

## Workaround for SCons scanning C++ files only when linking
SCons scans if a C++ file exist only at the linker stage. This led to the error that SCons tried to compile a procedurally generated C++ file
before its builder was called (and consequently, the C++ file was not existing on disk). The quick and dirty workaround: 
Add a custom command line option `--generate-procedural-code` and call a new SCons instance in the `SConstruct`:
```python
if not GetOption('help'):
    if not GetOption('generateProceduralCode'):
        os.system('scons --generate-procedural-code')

    if GetOption('generateProceduralCode'):
        SConscript('./build/proceduralFiles/SConscript')
```
The usage of `os.system()` is deliberate here to block the first SCons process from continuing until the procedural files are generated. 
Even though this is working, this approach could be a potential culprit for the issues I am having, so I will have to find a cleaner approach in the near future. 