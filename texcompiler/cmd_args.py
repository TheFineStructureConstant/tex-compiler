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
from texcompiler.utils import default

def buildCmdInput(**kwargs):
    '''
    Build command line argument parser 

     Outputs
    ---------
    Argument Parser Object
    '''
    # create parser object
    texParser = ArgumentParser(add_help = False)

    # add tex arguments
    if default(kwargs, 'add_tex_file', True): 
        texParser.add_argument(
            'texFile',
            type = str,
            nargs = '?',
            help = 'Name of the TeX file to compile. The ".tex" extension does not need to be included'
        )

    texParser.add_argument(
        '--tex-engine',
        type = str,
        required = False,
        dest = 'tex_engine',
        default = 'xelatex',
        help = 'Name of the TeX engine binary to use in compilation'
    )
    
    texParser.add_argument(
        '--tex-engine-path',
        type = str,
        required = False,
        default = '/usr/bin/',
        dest = 'tex_engine_path',
        help = 'Path to the TeX engine binary to use for compilation.\n'\
               'If no path is specified, the system default will be used.'
    )

    texParser.add_argument(
        '--bibtex-engine',
        type = str,
        required = False,
        dest = 'bibtex_engine',
        default = 'bibtex',
        help = 'Name of the BibTeX engine binary to use in compilation'
    )
    
    texParser.add_argument(
        '--bibtex-engine-path',
        type = str,
        required = False,
        default = '/usr/bin/',
        dest = 'bibtex_engine_path',
        help = 'Path to the BibTeX engine binary to use for compilation.\n'\
               'If no path is specified, the system default will be used.'
    )

    texParser.add_argument(
        '-html',
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
        action = "store_true",
        required = False,
        help = 'Clean up detritus from compilation. \n'\
             + 'Specifying this flag will remove all files with the name given in the '\
             + '"tex-file" positional argument with extensions specified by the "--rm-exts" flag.\n'\
             + 'If the "tex-file" positional argument is excluded, specifying this flage will\n'\
             + 'remove all files with extensions listed in the "--rm-exts" flag'
    ) 

    texParser.add_argument(
        '-y',
        '--yes',
        required = False,
        action = "store_true",
        help = 'Answer "yes" to any prompts'
    )

    return texParser

def parseTexCmdInputs():
    '''
      Parse arguments from command line

      Outputs
     ---------
      parsed arguments object
    '''
    # output parsed objects 
    texParser = buildCmdInput()
    return texParser.parse_args()
