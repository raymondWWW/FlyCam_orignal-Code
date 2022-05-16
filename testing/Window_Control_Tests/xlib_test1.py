"""
Get List of Windows using Python-xlib
"""

import Xlib
from Xlib.display import Display


newPIDs = []
DESIRED_NAME = "geany"

def get_absolute_geometry(win):
	"""
	Returns the (x, y, height, width) of a window relative to the
	top-left of the screen.
	"""
	geom = win.get_geometry()
	(x, y) = (geom.x, geom.y)
	
	print("Start")
	print(f"x: {x}, y: {y}")
	
	while True:
		parent = win.query_tree().parent
		pgeom = parent.get_geometry()
		x += pgeom.x
		y += pgeom.y
		
		if parent.id == root.id:
			# print("parent id matches root id. Breaking...")
			break
		win = parent
	
	print("End")
	print(f"x: {x}, y: {y}")

disp = Display()
root = disp.screen().root
children = root.query_tree().children

for win in children:
	winName = win.get_wm_name()
	pid = win.id
	
	if winName != None:
		if winName == "geany":
			print("======Children=======")
			print(f"winName: {winName}, pid: {pid}")
			get_absolute_geometry(win)
			
			print(f"{win.get_property()}")
			
			"""
			geom = win.get_geometry()
			print(f"geom: {geom}")
			print("*****parent*****")
			parent = win.query_tree().parent
			pgeom = parent.get_geometry()
			print(f"pgeom: {pgeom}")
			print(f"parent name: {parent.get_wm_name()}")
			"""
			print()
