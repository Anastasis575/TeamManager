import tkinter as tk
#credit to angeloped GithubGist
def make_textmenu(root):
	global the_menu
	the_menu = tk.Menu(root, tearoff=0)
	the_menu.add_command(label="Cut")
	the_menu.add_command(label="Copy")
	the_menu.add_command(label="Paste")
	the_menu.add_separator()
	the_menu.add_command(label="Select all")

def callback_select_all(event):
	# select text after 50ms
	root.after(50, lambda:event.widget.select_range(0, 'end'))

def show_textmenu(event):
	e_widget = event.widget
	the_menu.entryconfigure("Cut",command=lambda: e_widget.event_generate("<<Cut>>"))
	the_menu.entryconfigure("Copy",command=lambda: e_widget.event_generate("<<Copy>>"))
	the_menu.entryconfigure("Paste",command=lambda: e_widget.event_generate("<<Paste>>"))
	the_menu.entryconfigure("Select all",command=lambda: e_widget.select_range(0, 'end'))
	the_menu.tk.call("tk_popup", the_menu, event.x_root, event.y_root)

# bind the feature to all Entry widget
# root.bind_class("Entry", "<Button-3><ButtonRelease-3>", show_textmenu)
# root.bind_class("Entry", "<Control-a>", callback_select_all)