# -*- mode: python -*-
# SCons build file
import os
import sys

# DESCRIPTION: Add project directories containing required tools temporarily
# to Python path
# REMARK: Temporarily adding local directories to path variables
# is considered to be a security risk; however, no better solution available
# without installing the modules
sys.path.append(os.path.abspath("./tools/")) 
import MWE_Utilities as mweu

# DESCRIPTION: Target independent flags
TARGET_INDEPENDENT_CPP_FLAGS : list = ['-std=c++20', '-Wall']

##################################################################################
# DESCRIPTION: Define targets and sources for test routines ######################
##################################################################################
# REMARK: Do not specify file type for target, as it has to be adapted for each
# target platform individually
programTarget : str = 'bin/test' 
programSources : list = ['src/test.cpp']

##################################################################################
##################################################################################
# SECTION: SCONS: Configuration ##################################################
##################################################################################
##################################################################################
# DESCRIPTION: Constants
PROJECT_ROOT_DIRECTORY: str = mweu.getCurrentWorkingDirectory()
COMPILE_COMMANDS_FILE_PATH : str = 'config/compile_commands.json'

# DESCRIPTION: Supported target platforms
SUPPORTED_TARGET_PLATFORMS : list = ["linux.x86_64", "windows.amd64"]

# DESCRIPTION: Define host-target compatibility data base
# REMARK: Currently no cross-compilation implemented in this example due to the
# complexity, but available in original project
SUPPORTED_HOST_TARGET_COMBINATIONS : dict = {
    "linux.x86_64": ["linux.x86_64"],
    "windows.amd64": ["windows.amd64"]
}

# DESCRIPTION: Determine the host operating system for host system/target  
# system specific compilation settings
HOST_PLATFORM : str = mweu.getHostPlatform() 

###############################################################################
# DESCRIPTION: Custom command line options ####################################
###############################################################################
_tmp_helpString : str = 'Specifies the target platform for the compilation. '
_tmp_helpString += 'Allowed values: '
for _i,_platform in enumerate(SUPPORTED_TARGET_PLATFORMS):
    _tmp_helpString += '\"' + _platform 

    if _i != len(SUPPORTED_TARGET_PLATFORMS) - 1:
        _tmp_helpString += '\", '
_tmp_helpString += '\"all\".'

AddOption(
    '--target-platform',
    dest = 'targetPlatform',
    type = 'string',
    nargs = 1,
    action = 'store',
    help =  _tmp_helpString
)

_tmp_helpString = 'Switches off code compilation and only generates procedural '
_tmp_helpString += 'C++ files (and required helper files). Only to be used by '
_tmp_helpString += 'the SCons routine internally. (DIRTY HACK)'

AddOption(
    '--generate-procedural-code',
    dest = 'generateProceduralCode', 
    action = 'store_true',
    help = _tmp_helpString
)

###############################################################################
# DESCRIPTION: Setup of the SCons environment #################################
###############################################################################
env = Environment(
    COMPILATIONDB_USE_ABSPATH = True,
    CCFLAGS = TARGET_INDEPENDENT_CPP_FLAGS
)

# DESCRIPTION: Enable creation of compile_commands.json
env.Tool('compilation_db')

###############################################################################
# DESCRIPTION: Export important variables #####################################
###############################################################################
Export(
    'PROJECT_ROOT_DIRECTORY',
    'HOST_PLATFORM', 'COMPILE_COMMANDS_FILE_PATH', 
    'SUPPORTED_HOST_TARGET_COMBINATIONS',
    'programTarget', 'programSources', 'env'
)

###############################################################################
###############################################################################
# SECTION: Procedural file generation #########################################
###############################################################################
###############################################################################
# DESCRIPTION: Hack to trigger another run of SCons BEFORE starting the
# compilation. Only trigger when the --generate-procedural-code command
# line option is not already specified.
# REMARK: Specifiying it here ensures that the files will be created for all
# variants, but only if they do not exist already. In addition, the path is 
# not relative to the variant directory, but to the folder where the SConstruct
# is located
# REMARK: If statement required, so that no infinite loop can be 
# accidentally created
# REMARK: Necessary, since SCons in theory detects correctly the depedencies
# due to procedurally generated code, but fails to check it at the correct
# time: It is checked during linking, and not before compilation. So any
# compilation containing procedural code will fail if the procedural file(s)
# do/does not already exist. The trick is to start another instance of SCons 
# in the same thread, so that the first instance is halted until the second  
# one is finished. If the second one does not execute the target specific
# SConscripts, it will not abort due to compilation failure, but get to the
# step of procedural file compilation, which is otherwise impossible. This
# ensures that when the second instance of SCons is finished, all required 
# files are existing and valid, so that the compilation with the first
# SCons process can continue.
if not GetOption('help'):
    if not GetOption('generateProceduralCode'):
        print("\n[  START  ] Procedural Code Generation")
        os.system('scons --generate-procedural-code')
        print("[   END   ] Procedural Code Generation\n")

    if GetOption('generateProceduralCode'):
        SConscript('./build/proceduralFiles/SConscript')

###############################################################################
###############################################################################
# SECTION: Executable creation ################################################
###############################################################################
###############################################################################
# DESCRIPTION: Only procede to C++ compilation when not in generate procedural
# code mode
# REMARK: Ensures that procedural generation routine can be run and will not
# be stopped by C++ compilation errors  
if not GetOption('help'):
    if not GetOption('generateProceduralCode'):
        SConscript('./build/executables/SConscript')