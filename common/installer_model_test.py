import os;
import unittest
from appdescriptor import AppDescriptor
from installer_model import InstallerModel
from environment_model import EnvironmentModel
from nose.plugins.attrib import attr

@attr("unit", "installer_model")
class InstallerModelTest(unittest.TestCase):

	def setUp(self):
		self.name = "PowerTools Desktop"
		self.name_no_spaces = self.name.replace(" ", "")
		self.environment_model = EnvironmentModel()
		self.descriptor = AppDescriptor(os.path.dirname(os.path.realpath(__file__)) + r"\testfiles\xml\PowerToolsDesktop-app.xml")
		self.progam_files = "C:\\Program Files (x86)"
		self.name_and_version = self.name_no_spaces + "_3_0_11"
		self.install_dir = self.progam_files + os.sep + self.name_and_version
		self.sut = InstallerModel(descriptor = self.descriptor)

	def test_name_with_version_works(self):
		self.assertEqual(self.name_and_version, self.sut.name_with_version())

	def test_install_dir_works(self):
		self.assertEqual(self.install_dir , self.sut.install_dir())

	def test_exe_path_works(self):
		self.assertEqual(self.install_dir + os.sep + self.name_and_version + ".exe", self.sut.exe_path())

	def test_file_name_works(self):
		self.assertEqual(self.name_no_spaces + "-" + self.descriptor.version_number() + "-dev.exe", self.sut.file_name())

	def test_app_storage_folder_works(self):
		app_data = self.environment_model.app_data_path()
		self.assertEqual(app_data + os.sep + self.descriptor.app_id(), self.sut.app_storage_folder())

	def test_name_and_version_works(self):
		self.assertEqual(self.name + " 3.0.11" , self.sut.name_and_version())

	def test_powertools_xml_path_works(self):
		app_data = self.environment_model.app_data_path()
		self.assertEqual(app_data + os.sep + self.descriptor.app_id() + "\Local Store\powertools.xml", self.sut.powertools_xml_path())


@attr("unit", "installer_model")
class InstallerModelXTest(unittest.TestCase):

	def setUp(self):
		self.name = "PowerTools Desktop X"
		self.name_no_spaces = self.name.replace(" ", "")
		self.environment_model = EnvironmentModel()
		self.descriptor = AppDescriptor(os.path.dirname(os.path.realpath(__file__)) + r"\testfiles\xml\PowerToolsDesktopX-app.xml")
		self.progam_files = "C:\\Program Files (x86)"
		self.name_and_version = self.name_no_spaces + "_3_0_11"
		self.install_dir = self.progam_files + os.sep + self.name_and_version
		self.sut = InstallerModel(app_name = self.name, descriptor = self.descriptor)

	def test_name_with_version_works(self):
		self.assertEqual(self.name_and_version, self.sut.name_with_version())

	def test_install_dir_works(self):
		self.assertEqual(self.install_dir , self.sut.install_dir())

	def test_exe_path_works(self):
		self.assertEqual(self.install_dir + os.sep + self.name_and_version + ".exe", self.sut.exe_path())

	def test_file_name_works(self):
		name_without_x = self.name_no_spaces.replace("X", "")
		self.assertEqual(name_without_x + "-" + self.descriptor.version_number() + "-devx.exe", self.sut.file_name())

	def test_app_storage_folder_works(self):
		app_data = self.environment_model.app_data_path()
		self.assertEqual(app_data + os.sep + self.descriptor.app_id(), self.sut.app_storage_folder())

	def test_name_and_version_works(self):
		self.assertEqual(self.name + " 3.0.11" , self.sut.name_and_version())

	def test_powertools_xml_path_works(self):
		app_data = self.environment_model.app_data_path()
		self.assertEqual(app_data + os.sep + self.descriptor.app_id() + "\Local Store\powertools.xml", self.sut.powertools_xml_path())
