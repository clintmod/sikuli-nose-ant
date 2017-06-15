import os
import tempfile
from appdescriptor import AppDescriptor
from environment_model import EnvironmentModel

class InstallerModel(object):
	
	def __init__(self, app_name = "PowerTools Desktop", descriptor = None, env = "dev"):
		self.app_name = app_name
		self.environment_model = EnvironmentModel()
		self.descriptor = descriptor or AppDescriptor()
		self.env = env
		if("X" in self.app_name):
			self.env += "x"
		self.program_files_dir = "C:\Program Files (x86)"

	def name_without_spaces(self):
		return self.app_name.replace(" ", "")

	def name_with_version(self):
		return self.name_without_spaces() + "_" + self.descriptor.version_number().replace(".", "_")

	def install_dir(self):
		return self.program_files_dir + os.sep + self.name_with_version()
	
	def file_name(self):
		return "PowerToolsDesktop-" + self.descriptor.version_number() + "-" + self.env + ".exe"
	
	def exe_path(self):
		return self.install_dir() + os.sep + self.name_with_version() + ".exe"
	
	def installer_full_path(self):
		return tempfile.gettempdir() + os.sep + self.file_name()

	def app_storage_folder(self):
		app_data = self.environment_model.app_data_path()
		app_id = self.descriptor.app_id();
		return app_data + os.sep + app_id

	def name_and_version(self):
		return self.app_name + " " + self.descriptor.version_number()

	def powertools_xml_path(self):
		return self.app_storage_folder() + os.sep + "Local Store" + os.sep + "powertools.xml"