import os;
import unittest
import test_utils
from appdescriptor import AppDescriptor
from installer import Installer, InstallerModel 
from nose.plugins.attrib import attr
from nose.plugins.attrib import attr

@attr("unit", "installer", "installer_unit")
class InstallerUnitTest(unittest.TestCase):

	def setUp(self):
		self.model = InstallerModel()
		self.sut = Installer(self.model)

	def test_jenkins_project_name_works(self):
		self.sut = Installer()
		self.assertEqual("PowerToolsDesktop-head", self.sut.jenkins_project_name());
	
	def test_stop_server_works(self):
		self.sut.stop_server();

@attr("slow", "installer", "installer_aft")
class InstallerTest(unittest.TestCase):

	def setUp(self):
		test_utils.skip_if_group_failed_or_skipped("search")
		self.model = InstallerModel()
		self.sut = Installer(model = self.model)
 
	def tearDown(self):
		pass

	def test_reinstall_works(self):
		self.sut.reinstall();

@attr("slow", "installer", "installer_aft", "installer_x_aft")
class InstallerXTest(unittest.TestCase):

	def setUp(self):
		test_utils.skip_if_group_failed_or_skipped("search")
		self.model = InstallerModel("PowerTools Desktop X")
		self.sut = Installer(model = self.model)

	def test_reinstall_works(self):
		self.sut.reinstall();

@attr("slow", "installer", "installer_cleanup")
class InstallerCleanupTest(unittest.TestCase):

	def setUp(self):
		test_utils.skip_if_any_group_failed_or_skipped()
		self.model = InstallerModel()
		self.sut = Installer(model = self.model)
 
	def tearDown(self):
		pass

	def test_installer_cleanup(self):
		self.sut.uninstall()
		self.sut.delete_secret_folder()

@attr("slow", "installer", "installer_cleanup")
class InstallerXCleanupTest(unittest.TestCase):

	def setUp(self):
		test_utils.skip_if_any_group_failed_or_skipped()
		self.model = InstallerModel("PowerTools Desktop X")
		self.sut = Installer(model = self.model)
 
	def tearDown(self):
		pass

	def test_installerx_cleanup(self):
		self.sut.uninstall()
		self.sut.delete_secret_folder()