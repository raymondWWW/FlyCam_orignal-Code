from Xlib.display import Display


def printWindowHierachy(window, indent):
	children = window.query_tree().children
	for w in children:
		print(indent, w.get_wm_class())
		printWindowHierachy(w, indent+'-')


display = Display()
root = display.screen().root
print(f"root geom: {root.get_geometry()}")
printWindowHierachy(root, '-')
