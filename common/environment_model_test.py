import unittest
import os
from environment_model import EnvironmentModel
from nose.plugins.attrib import attr

@attr("unit", "environment_model")
class EnvironmentModelUnitTest(unittest.TestCase):

	def setUp(self):
		self.sut = EnvironmentModel()
	
	def tearDown(self):
		pass

	def test_app_data_path(self):
		self.assert_path_works(self.sut.app_data_path())

	def test_current_username(self):
		current_username = self.sut.current_username()
		self.assertIsNotNone(current_username)

	def test_cust_demo_path(self):
		self.assert_path_works(self.sut.cust_demo_path(), "Expected CUSTDEMO_HOME to be set")

	def test_cygwin_home(self):
		self.assert_path_works(self.sut.cygwin_home())

	def test_temp_dir(self):
		self.assert_path_works(self.sut.temp_dir())

	def test_java_home(self):
		self.assert_path_works(self.sut.java_home())

	def test_flex_home(self):
		self.assert_path_works(self.sut.flex_home())


	def assert_path_works(self, path, message = None):
		self.assertIsNotNone(path, message)
		assert os.path.exists(path), "Path does not exist: " + path
