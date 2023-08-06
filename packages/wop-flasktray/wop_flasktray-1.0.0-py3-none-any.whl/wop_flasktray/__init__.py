from pystray import Icon as icon, Menu as traymenu, MenuItem as item
import waitress
from PIL import Image, ImageDraw
import waitress

_trayIcon = None
_server = None

"""
Setting the tray icon with a menu

Keyword arguments:
	appname -- Name of the application
	logo -- filename to a picture
Return: None
"""
def setIcon(appname:str, logo:str, *menu)->None:
	global _trayIcon
	logoimage = None
	if logo != None:
		logoimage = Image.open(logo)
	_trayIcon = icon(appname,
		icon=logoimage, 
		menu=traymenu(*menu),
	)
	_trayIcon.run_detached()

"""
Stops the icon mainloop and closes the server
"""
def menuAction_quit()->None:
	global _trayIcon
	global _server
	_trayIcon.stop()
	_server.close()

"""
	Sets the tray icon and start the server.
	Keyword arguments:
		app -- flask app object
		host --  server's hostname or ip address
		port -- server's port number
		appname -- name of the application
		logo -- image filename of the tray icon
		*menu -- [optional] pystray.MenuItem tuple with custom menu items.

	Returns: None

	Example call with a custom menu. Multiple menu items possible as tuple.
		from pystray import MenuItem as item
		customMenu = (item("CustomMenuitem", action=customMenuFunc), <item...>)
		wop_flasktray.startIconServer(app, HOST, PORT, "Appname", customMenu)
	
	Without a custom menu parameter only the default "Quit"-item is visible.
"""
def startIconServer(app:object, host:str, port:int, appname:str, logo:str, *menu)->None:
	global _server
	defaultmenu = item("Beenden", action=menuAction_quit)
	_server = waitress.create_server(application=app, host=host, port=port)
	setIcon(appname, logo, *menu, defaultmenu)
	_server.run()
