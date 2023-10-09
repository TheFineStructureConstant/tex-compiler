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

import os
import subprocess

# setup paths with proper formatting
def formatPath(enginePath):
    if enginePath != '':
        if enginePath[-1] != '/':
            enginePath += '/'

    return enginePath


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
    texEngine       - Name of the tex engine binary to use
    texEnginePath   - Path to the specified tex engine 
    bibTexEngine    - Name of the bibtex engine binary to use
    packages        - list of paths to custom latex packages to compile in
    '''
    
    # extract keyword arguments 
    texEngine = kwargs['texEngine'] if 'texEngine' in kwargs else 'xelatex'
    texEnginePath = kwargs['texEnginePath'] if 'texEnginePath' in kwargs else ''  
    bibTexEngine = kwargs['bibTexEngine'] if 'bibTexEngine' in kwargs else 'bibtex'
    bibTexEnginePath = kwargs['bibTexEnginePath'] if 'bibTexEnginePath' in kwargs else ''  
    packages = kwargs['packages'] if 'packages' in kwargs else None

    # process keyword arguments
    texEnginePath = formatPath(texEnginePath)
    bibTexEnginePath = formatPath(bibTexEnginePath)

    # setup environment
    env = setupTexEnv(packages)

    # setup tex commands
    texCmd = [f'{texEnginePath}{texEngine}', texFile]
    bibtexCmd = [f'{bibTexEnginePath}{bibTexEngine}', texFile[:-4]]

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
