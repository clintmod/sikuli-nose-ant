import os
import tempfile
from utils import Shell

class EnvironmentModel(object):

	def __init__(self):
		self.shell = Shell(verbose=True)

	def get_env_variable(self, name, should_raise_errror = True):
		try:
			return os.environ[name]
		except Exception as e:
			return None
		
	def app_data_path(self):
		return self.get_env_variable("APPDATA")

	def current_username(self):
		return self.get_env_variable("USERNAME")

	def cust_demo_path(self):
		return self.get_env_variable("CUSTDEMO_HOME")

	def cygwin_home(self):
		return self.get_env_variable("CYGWIN_HOME")

	def java_home(self):
		return self.get_env_variable("JAVA_HOME")

	def flex_home(self):
		return self.get_env_variable("FLEX_HOME")

	def temp_dir(self):
		return tempfile.gettempdir()

	def workspace(self):
		return self.get_env_variable("WORKSPACE")
		