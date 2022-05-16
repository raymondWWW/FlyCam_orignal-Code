"""
Find Window Created by PySimple GUI

"""

import PySimpleGUI as sg

from Xlib.display import Display


def window_test():
	disp = Display()
	root = disp.screen().root
	children = root.query_tree().children

	for win in children:
		winName = win.get_wm_name()
		pid = win.id
		x, y, width, height = get_absolute_geometry(win, root)
		
		# if winName == None:
		if x == 300 and y == 20:
			
			print("======Children=======")
			print(f"winName: {winName}, pid: {pid}")
			print(f"x:{x}, y:{y}, width:{width}, height:{height}")
			# print(f"wm: {win.get_window_title()}")
			
			win.set_wm_name("New Window Name")
			
			# Move Window to the right 50 pixels
			win.configure(x=x+50)
			
			"""
			geom = win.get_geometry()
			# print(f"geom: {geom}")
			print("*****parent*****")
			parent = win.query_tree().parent
			pgeom = parent.get_geometry()
			print(f"pgeom: {pgeom}")
			print(f"parent name: {parent.get_wm_name()}")
			"""
			
			print()
			
			"""
			if winName == "geany":
				print("======Children=======")
				print(f"winName: {winName}, pid: {pid}")
				get_absolute_geometry(win, root)
				
				geom = win.get_geometry()
				print(f"geom: {geom}")
				print("*****parent*****")
				parent = win.query_tree().parent
				pgeom = parent.get_geometry()
				print(f"pgeom: {pgeom}")
				print(f"parent name: {parent.get_wm_name()}")
				print()
			"""



def get_absolute_geometry(win, root):
	"""
	Returns the (x, y, height, width) of a window relative to the
	top-left of the screen.
	"""
	geom = win.get_geometry()
	(x, y) = (geom.x, geom.y)
	
	# print("Start")
	# print(f"x: {x}, y: {y}")
	
	while True:
		parent = win.query_tree().parent
		pgeom = parent.get_geometry()
		x += pgeom.x
		y += pgeom.y
		
		if parent.id == root.id:
			# print("parent id matches root id. Breaking...")
			break
		win = parent
	
	# print("End")
	# print(f"x: {x}, y: {y}")
	return x, y, geom.width, geom.height


def main():
	print("Main")
	
	
	# Setup SG Theme
	sg.theme("LightGreen")
	
	# Setup Layout
	layout = [[sg.Button("Test Button", size=(15, 15))]]
	layout_p = [[sg.Text("Preview Window Text", size=(30, 10))]]
	
	# Setup Window
	window = sg.Window("Window Test", layout, location=(33, 10))
	window_p = sg.Window("Preview Window", layout_p, location=(300, 20))
	
	# Start While Loop
	while True:
		event, values = window.read(timeout=1)
		event_p, values_p = window_p.read(timeout=1)
		
		if event == sg.WIN_CLOSED or event_p == sg.WIN_CLOSED:
			break
		elif event == "Test Button":
			print("Test Button")
			window_test()
	
	pass


if __name__ == "__main__":
	main()
