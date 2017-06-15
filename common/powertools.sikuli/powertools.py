from sikuli import *
import os
import time
from utils import ScreenUtils
from os import path
import urllib2
from appdescriptor import AppDescriptor
from installer_model import InstallerModel
from shutil import copy

class PowerTools(object):

	def __init__(self,name=None, model=None):
		if name is None: name = "PowerTools Desktop"
		self.model = model or InstallerModel(app_name = name)

	def close(self):
		print "closing " + self.model.name_and_version()
		App.close(self.model.name_and_version())
		wait(1)

	def open(self):
		print "opening " + self.model.name_and_version()
		app = App(self.model.name_and_version())
		if not app.window():
			app = App.open(self.model.exe_path())
			wait(1)
		app.focus()
		wait("1417549996929.png", 60)
		#wait for the splash to disappear
		wait(3)
		return Region(app.window())
	
	def restart(self):
		self.close()
		return self.open()

	def focus(self):
		print "focusing " + self.model.name_and_version()
		app = App.focus(self.model.name_and_version())
		wait(1)
		if(app):
			return app.window()
		else :
			return None

	def copy_log_files_to_captures_dir(self, log_file = None):
		cur_date = time.strftime("%Y%m%d")
		log_file = log_file or "powertools_{0}.log".format(cur_date)
		src = path.join(self.model.app_storage_folder(), 'Local Store'
			, self.model.env, "projects"
			, log_file
		)
		if os.path.exists(src):
			sc = ScreenUtils()
			dest_dir = sc.captures_path
			copy(src, dest_dir)
			print "copied {0} to {1}".format(src, dest_dir)
		else :
			print "no log file found at " + src

