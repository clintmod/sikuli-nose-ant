import os; from os import path
import unittest
from time import sleep
from utils import Shell, XmlUtils, ScreenUtils
from nose.plugins.attrib import attr
from nose.tools import raises

@attr("unit", "utils", "xml_utils")
class XmlUtilsTest(unittest.TestCase):
 
	def setUp(self):
		pass
 
	def tearDown(self):
		pass
	
	def test_assertElementsEqual_works_whenElementsAreEqual(self):
		XmlUtils.assertElementsEqual (
			  file_path = path.join(path.dirname(__file__), 'testfiles/xml/list.xml')
			, element_xpath = "./coderefs/coderef[@name='roof-type']/options/option[@value='Palm Fronds']"
			, expected_xml_string = '<option value="Palm Fronds" name="Palm Fronds" />'
		)
	@raises(Exception)
	def test_assertElementsEqual_works_whenElementsAreNotEqual(self):
		file_path = path.join(path.dirname(__file__), 'testfiles/xml/list.xml')
		XmlUtils.assertElementsEqual (
			  file_path = file_path
			, element_xpath = "./coderefs/coderef[@name='roof-type']/options/option[@value='Palm Fronds']"
			, expected_xml_string = '<option value="Palm Fronds 2" name="Palm Fronds" />'
		)

	@raises(Exception)
	def test_assertElementsEqual_works_whenXPathNotFound(self):
		XmlUtils.assertElementsEqual (
			  file_path = path.join(path.dirname(__file__), 'testfiles/xml/list.xml')
			, element_xpath = "./coderefs2/coderef[@name='roof-type']/options/option[@value='Palm Fronds']"
			, expected_xml_string = '<option value="Palm Fronds" name="Palm Fronds" />'
		)
	@raises(Exception)
	def test_assertElementsEqual_works_when_fileNotFound(self):
		XmlUtils.assertElementsEqual (
			  file_path = "asdf"
			, element_xpath = "./coderefs/coderef[@name='roof-type']/options/option[@value='Palm Fronds']"
			, expected_xml_string = '<option value="Palm Fronds" name="Palm Fronds" />'
		)

	def test_updateElementAttributeValue_works(self):
		file_path = path.join(path.dirname(__file__), 'testfiles/xml/update.xml')
		element_xpath = "./property[@name='modelID']";
		expected = "asdf"
		attribute = "value"
		XmlUtils.updateElementAttributeValue(
			  file_path = file_path
			, element_xpath =  element_xpath
			, attribute = attribute
			, new_value = expected
		)
		actual = XmlUtils.getElement(file_path, element_xpath)
		self.assertEquals(expected, actual.get(attribute))

	def test_getElementAttributeValue_works(self):
		file_path = path.join(path.dirname(__file__), 'testfiles/xml/update.xml')
		element_xpath = "./property[@name='customerID']";
		expected = "custDEMO"
		attribute = "value"
		actual = XmlUtils.getElementAttributeValue(
			  file_path = file_path
			, element_xpath =  element_xpath
			, attribute = attribute
		)
		
		self.assertEquals(expected, actual) 

	def test_updateElementText_works(self):
		file_path = path.join(path.dirname(__file__), 'testfiles/xml/eclipse.project')
		element_xpath = "./name";
		expected = "asdf"
		XmlUtils.updateElementText(
			  file_path = file_path
			, element_xpath =  element_xpath
			, new_value = expected
		)


@attr("unit", "utils", "shell")
class ShellTest(unittest.TestCase):

	def setUp(self):
		self.sut = Shell(verbose=False)

	def tearDown(self):
		pass

	def test_execute(self):
		result = self.sut.execute("echo Clint is cool")
		self.assertEquals(result, "Clint is cool")

	@raises(Exception)
	def test_execute_fails_ok(self):
		result = self.sut.execute("expecting_this_to_fail")

	def test_execute_in_background_works(self):
		process_name = "calc"
		self.sut.execute_in_background(process_name)
		sleep(0.5)
		self.sut.kill_process(process_name+".exe")

	def test_exe_exists_on_path_returns_True(self):
		self.assertTrue(self.sut.exe_exists_on_path("java"))

	def test_exe_exists_on_path_returns_False(self):
		self.assertFalse(self.sut.exe_exists_on_path("asdf"))

@attr("unit", "utils", "screen")
class ScreenUtilsUnitTest(unittest.TestCase):

	def setUp(self):
		self.sut = ScreenUtils(captures_path = "../captures")
	
	def tearDown(self):
		pass
	
	def test_capture_screen(self):
		self.sut.capture_screen(False)

	def test_video_capture_works(self):
		self.sut.start_video_capture()
		sleep(2)
		self.sut.stop_video_capture()

