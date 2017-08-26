from sikuli import *
import subprocess
from subprocess import CalledProcessError
import os
import shutil
from nose.tools import assert_equal

try:
	import xml.etree.cElementTree as ET
except:
	import xml.etree.ElementTree as ET

class XmlUtils(object):
	@staticmethod
	def assertElementsEqual(file_path, element_xpath, expected_xml_string):
		expected_element = ET.fromstring(expected_xml_string)
		actual_element = XmlUtils.getElement(file_path, element_xpath)
		if (actual_element is None):
			raise Exception("Element not found for file at: " + file_path + " with xpath " + element_xpath)
		expected = ET.tostring(expected_element).strip()
		actual = ET.tostring(actual_element).strip()
		print expected
		print actual
		assert_equal(expected, actual)

	@staticmethod
	def updateElementAttributeValue(file_path, element_xpath, attribute, new_value):
		tree = ET.parse(file_path)
		element = tree.find(element_xpath)
		if element is None:
			raise Exception("no element found for xpath: {0} in file: {1}".format(element_xpath, file_path))
		element.set(attribute, new_value)
		tree.write(file_path)

	@staticmethod
	def getElementAttributeValue(file_path, element_xpath, attribute):
		tree = ET.parse(file_path)
		element = tree.find(element_xpath)
		if element is None:
			raise Exception("no element found for xpath: {0} in file: {1}".format(element_xpath, file_path))
		return element.get(attribute)

	@staticmethod
	def getElement(file_path, element_xpath):
		try :
			tree = ET.parse(file_path)
		except Exception as e:
			return None
		element = tree.find(element_xpath)
		return element

	@staticmethod
	def elementToString(element):
		return ET.tostring(element)

	@staticmethod
	def updateElementText(file_path, element_xpath, new_value):
		tree = ET.parse(file_path)
		element = tree.find(element_xpath)
		if element is None:
			raise Exception("no element found for xpath: {0} in file: {1}".format(element_xpath, file_path))
		element.text = new_value
		tree.write(file_path)


class Shell(object):

	def __init__(self, verbose = False):
		self.all_verbose = verbose

	def execute(self, command, cwd = ".", suppress_errors=False, verbose = False):
		output = ""
		verbose = verbose or self.all_verbose
		if(verbose):
			print "\n--- executing shell command ----\n"
			print "setting working dir to: " + cwd
			print "command: " + command
			
		try:
			output = subprocess.check_output(command, shell=(verbose), cwd=cwd, stderr=subprocess.STDOUT).strip()
			if(verbose):
				print "output = " + output
		except CalledProcessError as e:
			print "Error Info:\nerror code = {0}\ncmd {1}\nerror message: {2}".format(e.returncode, e.cmd, e.output)
			if (suppress_errors == False): raise
		finally:
			if(verbose):
				print "---- shell execution finished ---\n" 
		return output

	def execute_in_background(self, command, cwd = "."):
		try:
			subprocess.Popen(command, shell = True)
		except Exception as e:
			print str(e)

	def kill_process(self, process_name):
		self.execute("taskkill /F /IM " + process_name)

	def exe_exists_on_path(self, exe_name):
		try:
			self.execute("which " + exe_name)
		except:
			return False
		return True

class ScreenUtils(object):

	def __init__(self, captures_path = None):
		self.screen = Screen()
		self.shell = Shell(verbose = False)
		try:
			env_captures_path = os.environ["CAPTURES_DIR"]
		except Exception as e:
			env_captures_path = "../captures"
		self.captures_path = captures_path or env_captures_path
		self.ensure_captures_dir_is_created()
		
	def capture_screen(self, verbose = True):
		file = self.screen.capture(self.screen.getBounds())
		file_name = str(file).split(os.sep).pop(-1)
		new_path = self.captures_path + os.sep + file_name
		shutil.copyfile(file, new_path)
		if verbose: 
			print ("\ncaptured screen shot at " + new_path + "\n")
		return new_path

	def clean_captures(self):
		shutil.rmtree(self.captures_path, self.rmtree_error_handler)
	
	def rmtree_error_handler(func, path, execinfo): 
		print "Error deleting captures"

	def ensure_captures_dir_is_created(self, captures_path = None):
		captures_path = captures_path or self.captures_path
		if not os.path.exists(captures_path):
			os.makedirs(captures_path)
		assert os.path.exists(captures_path)

	def start_video_capture(self, output_file_name = None):
		output_file_name = output_file_name or "afts"
		if not self.shell.exe_exists_on_path("ffmpeg"):
			print "warning ffmpeg not found on path"
		else:
			output_file_path = os.path.join(self.captures_path, output_file_name + ".flv")
			self.shell.execute_in_background("ffmpeg -y -loglevel error -f gdigrab -i desktop " + output_file_path)

	def stop_video_capture(self):
		try:
			self.shell.kill_process("ffmpeg.exe")
		except:
			pass
