import os as _os
import wx as _wx


def makeicon(path):
	"""
	path: image's full path 
	
	returns an icon
	"""
	if(isinstance(path, str) == False):
		raise TypeError("path must be of type string")
	
	FullPath = path
	

	if(_os.path.isabs(FullPath) == False):
		raise ValueError(path + " is relative path, full path expected.")
		
	
	
	if(_os.path.exists(FullPath) == False):
		raise ValueError("Invalid path: " + path)

	icon = _wx.Icon()
	image = _wx.Image()
	image.LoadFile(FullPath)
	bmp=image.ConvertToBitmap()
	icon.CopyFromBitmap(bmp)

	return icon


