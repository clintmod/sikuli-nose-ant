import os;
import unittest
import test_utils
from workspace import Workspace
from powertools import PowerTools
from installer_model import InstallerModel
from nose.plugins.attrib import attr

powertools = PowerTools()

@attr("unit", "workspace", "workspace_unit")
class WorkspaceUnitTest(unittest.TestCase):
	def setUp(self):
		self.workspace = Workspace()
 
	def tearDown(self):
		pass

	def test_ssh_dir(self):
		ssh_dir = self.workspace.ssh_dir()
		self.assertIsNotNone(ssh_dir)
	


@attr("slow", "workspace", "workspace_aft")
class WorkspaceTest(unittest.TestCase):
	
	def setUp(self):
		test_utils.skip_if_group_failed_or_skipped("powertools_aft")
		self.workspace = Workspace()
	
	def tearDown(self):
		pass

	def test_1_remove_configuration_works(self):
		self.workspace.remove_configuration()

	def test_2_configure_if_required_works(self):
		powertools.restart()
		result = self.workspace.configure_if_required()
		self.assertTrue(result, "Workspace config screen should be there.")
		
	def test_3_configure_if_required_works_when_not_required(self):
		powertools.restart()
		result = self.workspace.configure_if_required()
		self.assertFalse(result, "Workspace config screen should not be there.")
