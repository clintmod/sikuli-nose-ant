import unittest
import os
from config import Config
from nose.plugins.attrib import attr
from environment_model import EnvironmentModel
import shutil

env_model = EnvironmentModel()

base_folder = env_model.workspace() or env_model.cust_demo_path() or os.path.expanduser("~")
test_config_file_path = os.path.join(base_folder, "config-test.json")

@attr("unit", "config")
class ConfigOrderedUnitTest(unittest.TestCase):
	
	def setUp(self):
		self.sut = Config(config_file_path = test_config_file_path)
		self.sut.delete_config()
		if not os.path.exists("temp"):
			os.makedirs("temp")

	def tearDown(self):
		self.sut.delete_config()
		shutil.rmtree("temp")

	def test_current_project_path(self):
		self.assertIsNone(self.sut.current_project_path)
		self.sut.current_project_path = "temp"
		self.assertEqual("temp", self.sut.current_project_path)
		self.sut.flush_config()
		self.assertIsNone(self.sut.current_project_path)
		self.sut.load_config()
		self.assertEqual("temp", self.sut.current_project_path)
		self.sut.current_project_path = None
		self.assertIsNone(self.sut.current_project_path)
		self.sut.flush_config()
		self.sut.load_config()
		self.assertIsNone(self.sut.current_project_path)

@attr("unit", "config")
class ConfigUnitTest(unittest.TestCase):
	''' Test that we can call the methods independantly '''
	def setUp(self):
		self.sut = Config(config_file_path = test_config_file_path)

	def tearDown(self):
		self.sut.delete_config()

	def test_current_project_path(self):
		path = self.sut.current_project_path

	def test_set_current_project_path(self):
		self.sut.set_current_project_path = "asdf"

	def test_save_config(self):
		self.sut.save_config()

	def test_load_config(self):
		self.sut.load_config()

	def test_flush_config(self):
		self.sut.flush_config()

	def test_set_property_value(self):
		self.sut.set_property_value("asdf", "asdf2")
		self.assertEqual("asdf2", self.sut.get_property_value("asdf"))

	def test_get_property_value(self):
		self.sut.set_property_value("asdf", "blah")
		self.assertEqual("blah", self.sut.get_property_value("asdf"))
