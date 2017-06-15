import unittest
import os
from appdescriptor import AppDescriptor
from nose.plugins.attrib import attr

@attr("unit", "appdescriptor")
class AppDescriptorTest(unittest.TestCase):
 	
	def setUp(self):
		self.sut = AppDescriptor()
		self.sut.file_path = os.path.dirname(os.path.realpath(__file__)) + r"\testfiles\xml\PowerToolsDesktop-app.xml"
 	
	def tearDown(self):
		pass
	
	def test_version_number_works(self):
		self.assertEqual("3.0.11", self.sut.version_number())

	def test_version_label_works(self):
		self.assertEqual("v3.0.11.1 (HEAD)", self.sut.version_label())
	
	def test_app_id_works(self):
		self.assertEqual("com.somecompany.powertools.PowerToolsDesktop.3.0.11", self.sut.app_id())
