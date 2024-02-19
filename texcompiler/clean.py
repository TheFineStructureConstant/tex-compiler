import subprocess
from pathlib import Path

from texcompiler.defaults import rmExts
from texcompiler.utils import default

def clean(**kwargs):
    
    # get paths to files
    paths = []
    for ext in rmExts:
        for path in Path().rglob(f'*.{ext}'):
            paths.append(path)
    
    # prompt for user input if desired
    if len(paths) == 0:
        print('No files to remove')
        exit()

    if not default(kwargs, 'yes', False):
        msg = 'Files to remove:\n'
        msg += 20 * '=-' + '=\n'
        for path in paths: msg += (f'{path}\n')
        msg += 20 * '=-' + '=\n'
        msg += 'Remove these files? [y/n]: '
        
        inputVal = input(msg)
        accepted = 'y' in inputVal and not 'n' in inputVal 

        if not accepted: 
            exit()

    # remove files
    cmd = ['rm'] 
    for path in paths: 
        cmd.append(path)

    subprocess.run(cmd)
    print('Files removed!')
