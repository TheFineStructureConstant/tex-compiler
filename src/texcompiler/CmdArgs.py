################################################################################
#   
#   Author:          J. Pate 
#   github username: TheFineStructureConstant
#   email:           patex019@umn.edu
#   Date:            10/1/2023
#   License:         MIT License
#
#   Description:
#   Construct command line parser for the build script 
#
################################################################################

from argparse import ArgumentParser

from texcompiler.defaults import rmExts

def parseTexCmdInputs():
    '''
      Parse arguments from command line

      Outputs
     ---------
      parsed arguments object
    '''
    
    # create parser object
    texParser = ArgumentParser()

    # add tex arguments
    texParser.add_argument(
        'tex-file',
        type = str,
        nargs = '?',
        help = 'Name of the TeX file to compile. The ".tex" extension does not need to be included'
    )

    texParser.add_argument(
        '--tex-engine',
        type = str,
        required = False,
        dest = 'texEngine',
        default = 'xelatex',
        help = 'Name of the TeX engine binary to use in compilation'
    )
    
    texParser.add_argument(
        '--tex-engine-path',
        type = str,
        required = False,
        default = '/usr/bin/xelatex',
        dest = 'texEnginePath',
        help = 'Path to the TeX engine binary to use for compilation.\n'\
               'If no path is specified, the system default will be used.'
    )

    texParser.add_argument(
        '--html',
        action = "store_false",
        required = False,
        dest = 'outputHTML',
        help = 'Compile TeX document as an HTML document instead of a PDF document'
    )

    texParser.add_argument(
        '--rm-exts',
        type = str,
        nargs = '+',
        required = False,
        dest = 'rmExts',
        help = f'File types to remove. Default: {rmExts}'
    )

    texParser.add_argument(
        '-c',
        '--clean',
        action = "store_false",
        required = False,
        help = 'Clean up detritus from compilation. \n'\
             + 'Specifying this flag will remove all files with the name given in the '\
             + '"tex-file" positional argument with extensions specified by the "--rm-exts" flag.\n'\
             + 'If the "tex-file" positional argument is excluded, specifying this flage will\n'\
             + 'remove all files with extensions listed in the "--rm-exts" flag'
    ) 

    # output parsed objects 
    return texParser.parse_args()

