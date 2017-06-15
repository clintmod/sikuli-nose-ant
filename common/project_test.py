import unittest
import test_utils
from project import Project
from powertools import PowerTools
from nose.plugins.attrib import attr

project = Project()
powertools = PowerTools()

@attr("slow", "project", "project_aft")
class ProjectTest(unittest.TestCase):

	def setUp(self):
		test_utils.skip_if_group_failed_or_skipped("template_aft")
		powertools.focus()
	
	def tearDown(self):
		pass

	def test_1_restart_powertools(self):
		powertools.restart()

	def test_2_open_or_create_or_join(self):
		project.open_or_create_or_join()
		

@attr("cleanup", "project", "project_cleanup")
class ProjectCleanUpTest(unittest.TestCase):
	
	def setUp(self):
		powertools.focus()

	def test_delete_locally_and_from_server_works(self):
		test_utils.skip_if_any_group_failed_or_skipped();
		project.delete_locally_and_from_server()

@attr("slow", "project", "project_dev")
class ProjectDevTest(unittest.TestCase):
	
	def setUp(self):
		powertools.focus()

	def test_1_click_open_or_create_menu_item_works(self):
		project.click_open_or_create_menu_item()

	def test_2__open_works(self):
		project._open()