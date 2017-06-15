import unittest
import test_utils
from powertools import PowerTools
from nose.plugins.attrib import attr

@attr("slow", "powertools", "powertools_aft")
class PowerToolsTest(unittest.TestCase):

	def setUp(self):
		test_utils.skip_if_group_failed_or_skipped("installer_aft")
		self.ptx = PowerTools("PowerTools Desktop X")
		self.pt = PowerTools("PowerTools Desktop")

	@classmethod
	def tearDownClass(cls):
		ptx = PowerTools("PowerTools Desktop X")
		ptx.close()
		pt = PowerTools("PowerTools Desktop")
		pt.close()

	def test_1_open(self):
		self.open_both()
		#call it twice to make sure it doesn't fail
		self.open_both()

	def test_2_focus_both(self):
		self.focus_both()
		#called twice to make sure it doesn't fail
		self.focus_both()

	def test_3_restart(self):
		self.restart_both()
		#called twice to make sure it doesn't fail
		self.restart_both()

	def test_4_close(self):
		self.close_both()
		#called twice to make sure it doesn't fail
		self.close_both()


#-- helper methods --

	def open_both(self):
		ptwin = self.pt.open()
		self.assertIsNotNone(ptwin)
		ptxwin = self.ptx.open()
		self.assertIsNotNone(ptxwin)

	def close_both(self):
		self.ptx.close()
		self.assertIsNone(self.ptx.focus())
		self.pt.close()
		self.assertIsNone(self.pt.focus())
		
	def restart_both(self):
		ptwin = self.pt.restart()
		self.assertIsNotNone(ptwin)
		ptxwin = self.ptx.restart()
		self.assertIsNotNone(ptxwin)

	def focus_both(self):
		ptwin = self.pt.focus()
		self.assertIsNotNone(ptwin)
		ptxwin = self.ptx.focus()
		self.assertIsNotNone(ptxwin)

@attr("unit", "powertools", "aft_artifact_archival")
class PowerToolsUnitTest(unittest.TestCase):

	def setUp(self):
		self.pt = PowerTools("PowerTools Desktop")

	def tearDown(self):
		pass

	def test_that_copy_log_files_to_captures_dir_works(self):
		self.pt.copy_log_files_to_captures_dir()

	def test_that_copy_log_files_to_captures_dir_works_when_no_log_file_exists(self):
		self.pt.copy_log_files_to_captures_dir(log_file = "asdf.log")
