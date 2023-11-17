#!/usr/bin/env python3
import texcompiler

# get args and compile document
cmdArgs = texcompiler.parseTexCmdInputs()

if cmdArgs.clean:
    print("Will clean eventually")
    print(texcompiler.defaults.rmExts)

else:
    print(cmdArgs)
    texcompiler.compileTeX(
        cmdArgs.texFile,
        texEngine = cmdArgs.texEngine,
        texEnginePath = cmdArgs.texEnginePath,
        bibTexEnginePath = cmdArgs.bibTexEnginePath,
        bibTexEngine = cmdArgs.bibTexEngine,
    )
