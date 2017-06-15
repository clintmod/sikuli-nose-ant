import os
import urllib2
import tempfile
from utils import Shell
from appdescriptor import AppDescriptor
from environment_model import EnvironmentModel
from installer_model import InstallerModel
from powertools import PowerTools

class Installer(object):

	def __init__(self, model=None, shell=None, powertools=None):
		#side step the circular module level import
		self.shell = shell or Shell()
		self.model = model or InstallerModel()
		self.environment_model = EnvironmentModel()
		self.powertools = powertools or PowerTools(model = model)

	def stop_server(self):
		self.shell.execute("wmic process Where \"CommandLine Like '%powertools%' and name like '%javaw%'\" call terminate")

	def uninstall(self):
		self.stop_server()
		self.powertools.close()
		self.shell.execute("wmic product where \"name like '%" + self.model.app_name + " " + self.model.descriptor.version_number() + "%'\" call uninstall")
		self.shell.execute("rm -rf '" + self.model.install_dir() + "'")
		print self.model.install_dir()
		assert os.path.exists(self.model.install_dir()) == False

	def delete_secret_folder(self):
		self.shell.execute("rm -rf " + self.model.app_storage_folder())
		assert os.path.exists(self.model.app_storage_folder()) == False

	def install(self):
		self.shell.execute(self.model.installer_full_path() + " -silent -eulaAccepted -allowDownload -desktopShortcut -programMenu")

	def reinstall(self):
		self.download()
		self.uninstall()
		self.install()

	def download(self):
		download_url = "http://jenkins.somecompany.net:8080/job/" + self.jenkins_project_name() 
		download_url += "/lastSuccessfulBuild/artifact/dist/" + self.model.file_name()
		orig_dir = os.getcwd()
		os.chdir(self.environment_model.temp_dir())
		stream = urllib2.urlopen(download_url)
		output = open(self.model.file_name(), 'wb')
		output.write(stream.read())
		output.close()
		os.chdir(orig_dir)
		print "Installer downloaded to: " + self.model.installer_full_path()

	def jenkins_project_name(self):
		if("HEAD" in self.model.descriptor.version_label()):
			return "PowerToolsDesktop-head"
		else :
			return "PowerToolsDesktop-spi_" + self.model.descriptor.version_number().replace(".", "_")

