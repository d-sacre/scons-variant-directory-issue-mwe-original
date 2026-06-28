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
If you specify a target platform that is different to your host platform, the build tool
will halt with an error (cross-compilation is not implemented in this MWE).
