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
import os
import subprocess

rmExts = ['aux', 'log', 'bbl', 'blg', 'pdf']

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

# setup environment for custom tex packages
def setupTexEnv(packages):

    # construct texInputs
    env = os.environ
    texInputs = '.:'

    if packages is not None:
        for entry in packages:
            
            count = 0
            for char in reversed(entry[-2:]):
                if char == '/':
                    count += 1

            prefix = './'
            value = entry
            if '/' == entry[0]:
                prefix = '' 
            elif './' == entry[0:2]:
                prefix = ''
            elif '../' == entry[0:3]:
                prefix = ''
            elif '~/' == entry[0:2]:
                prefix = os.path.expanduser('~') 
                value = entry[1:]
            
            texInputs += f"{prefix}{value}{(2-count)*'/'}:"
            
            
        # construct and return environment
        env['TEXINPUTS'] = texInputs

    return env


# compile tex project
def compileTeX(texFile, **kwargs):
    '''
    Description: Compile tex document with specified options

    Arguments
    =========

    Positional
    ----------
    texFile - name of the base tex file to compile

    Keyword
    -------
    texEngine    - Name of the tex engine binary to use
    bibTexEngine - Name of the bibtex engine binary to use
    packages     - list of paths to custom latex packages to compile in
    '''
    
    # extract keyword arguments 
    texEngine = kwargs['texEngine'] if 'texEngine' in kwargs else 'xelatex'
    bibTexEngine = kwargs['bibTexEngine'] if 'bibTexEngine' in kwargs else 'bibtex'
    packages = kwargs['packages'] if 'packages' in kwargs else None

    # setup environment
    env = setupTexEnv(packages)

    # setup tex commands
    texCmd = [f'{texEngine}', texFile]
    bibtexCmd = [bibTexEngine, texFile[:-4]]

    # check if the document has a bibtex bibliography
    hasBibtex = False
    with open(texFile, 'r') as texFile:
        for line in texFile:
            if '\\bibliography' in line:
                hasBibtex = True
                break
    
    # compile the document
    try: 
        subprocess.run(texCmd, env = env).check_returncode()
        if hasBibtex:
            subprocess.run(bibtexCmd, env = env).check_returncode()
            subprocess.run(texCmd, env = env).check_returncode()
            subprocess.run(texCmd, env = env).check_returncode()

    except subprocess.CalledProcessError as e:
        if e.stdout is None:
            print(f'TeX compilation command {" ".join(e.cmd)} failed')
        else:
            print(f'TeX compilation command {" ".join(e.cmd)} failed with error:')
            print(f'{e.stdout}')


if __name__ == "__main__":
    compileTeX('test.tex', packages = ['test//', '~/testtest'])
