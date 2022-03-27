# -*- coding: utf-8 -*-

# FreeCAD macro for woodworking to apply and store textures
# Author: Darek L (aka dprojects)
# Version: 1.0 (total prototype)
# Latest version: https://github.com/dprojects/setTextures

import FreeCADGui
from PySide import QtGui
from pivy import coin
import urllib.request
import tempfile
import os

with tempfile.TemporaryDirectory() as tmpDir:
	FreeCAD.Console.PrintMessage("\n Directory: "+tmpDir)

	#for obj in FreeCADGui.Selection.getSelection():
	for obj in FreeCAD.activeDocument().Objects:
	
		if str(obj.Label2) == "":
			continue

		textureURL = str(obj.Label2)
		data = urllib.request.urlopen(textureURL)

		texFilename = os.path.join(tmpDir, obj.Label)
		out = open(str(texFilename), "wb")
		out.write(data.read())
		out.close()
	
		FreeCAD.Console.PrintMessage("\n File: "+texFilename)

		rootnode = obj.ViewObject.RootNode
		texture =  coin.SoTexture2()
		texture.filename = texFilename

		skip = 0
		for i in rootnode.getChildren():
			if hasattr(i, "filename"):
				i.filename = ""
				i.filename = texFilename
				skip = 1

		if skip == 0:
			rootnode.insertChild(texture, 1)
				
