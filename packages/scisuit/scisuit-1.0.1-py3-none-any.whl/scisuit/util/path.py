import os as _os
import sys as _sys

"""
The function name is similar to std::filesystem::path::parent_path (in C++)
"""

def parent_path(Path, level = 0):
	"""
	Path: A relative or full path
	
	If Path = C:\\a\\b\\c.py
	
	if level=0, returns C:\\a\\b 
	if level = 1, returns C:\\a
	
	"""
	if(isinstance(Path, str) == False):
		raise TypeError("path must be of type string")
	
	PathList = _os.path.normpath(Path).split(_os.sep)
	
	NElems = level + 1
	if NElems>len(PathList):
		raise ValueError("Requested level exceeds the depth of Path")

	del PathList[-NElems::]
	
	#join the list using the default os separator
	ParentPath = _os.sep.join(PathList) + _os.sep
	
	return ParentPath



def pyhomepath():
	"""
	returns the Python Home Path
	"""
	return _sys.exec_prefix
