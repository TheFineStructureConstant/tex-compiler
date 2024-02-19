################################################################################
#   
#   Author:          J. Pate 
#   github username: TheFineStructureConstant
#   email:           patex019@umn.edu
#   Date:            10/1/2023
#   License:         MIT License
#
#   Description:
#   default parameters for the texcompiler package
#
################################################################################

# default list of file extensions to remove during cleaning
texExts = ['aux', 'log', 'out', 'pdf']
bibTexExts = ['bbl', 'blg']
rmExts = [*texExts, *bibTexExts]
