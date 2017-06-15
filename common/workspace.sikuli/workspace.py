from sikuli import *
import os
import tempfile
from search import flex_label, flex_button
from installer_model import InstallerModel
from environment_model import EnvironmentModel

user_id_label = flex_label(text = "User ID", font_color = "FFFFFF")

class Workspace(object):
	def __init__(self):
		self.installer_model = InstallerModel()
		self.environment_model = EnvironmentModel()

	def configure_if_required(self, user = None, passwd = None):
		print "checking for workspace config screen"
		
		if (exists(user_id_label, 3) is None):
			print "workspace config not found"
			return False
		else:
			print "workspace config found... configuring"
			self.configure(user, passwd)
			return True
     
	def configure(self, user = None, passwd = None):
		self.user = user or "clint.modien@somecompany.com"
		self.passwd = passwd or "asdf"
		region = find(user_id_label).right(10).right(30)
		doubleClick(region)
		paste(self.user)
		type(Key.TAB)
		paste(self.passwd)
		type(Key.TAB)
		paste(self.environment_model.java_home())
		type(Key.TAB)
		type(Key.TAB)
		type(Key.TAB)
		type(Key.TAB)
		type(Key.TAB)
		paste(self.ssh_dir() + os.sep + "spibuild02")
		type(Key.TAB)
		type(Key.TAB)
		hosts_file =  tempfile.gettempdir() + os.sep + "known_hosts"
		open(hosts_file,'w').close()
		paste(hosts_file)
		option = find("1418932236903.png")
		region = option.right(30)
		if region.exists("1418932432212.png", .2) is not None:
			click(option)

		option = find("1418938582026.png")
		region = option.right(30).grow(5)
		if region.exists("1418932432212.png", .2) is None:
			click(option)
		click("1418938742184.png")
		didVanish = waitVanish("1418938742184.png",5)
		if(didVanish == False):
			if(exists("1425944771805.png") != None):
				raise Exception("Invalid or Unauthorized User ID")
			else:
				raise Exception("An unknown error occured configuring the workspace.")

	def remove_configuration(self):
		if os.path.exists(self.installer_model.powertools_xml_path()):
			os.remove(self.installer_model.powertools_xml_path())

	def ssh_dir(self):
		cygwin_home = self.environment_model.cygwin_home()
		return cygwin_home + os.sep + "home" + os.sep + self.environment_model.current_username() + os.sep + ".ssh"
