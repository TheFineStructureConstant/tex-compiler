
################################################################################
#
#   Function: Extract keyword arguments with default value
#
################################################################################
#
#   Inputs
#  --------
#   kwargs      - keyword argument dictionary
#   key         - key to extract from the dictionary 
#   default     - (OPTIONAL) default value to return if key is not found
#
#   Outputs
#  ---------
#   kwargs evaluated at key if key is available otherwise default value
#
################################################################################
def default(kwargs, key, default = None)
    return kwargs[key] if key in kwargs else default
