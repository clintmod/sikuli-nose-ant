import unittest
import os
import test_utils
from config import Config
from powertools import PowerTools
from environment_model import EnvironmentModel
from template import ProjectTemplate, nix_sep
from utils import Shell
from nose.plugins.attrib import attr

env_model = EnvironmentModel()

base_folder = env_model.workspace() or env_model.cust_demo_path() or os.path.expanduser("~")
test_config_file_path = os.path.join(base_folder, "..", "config-test.json")

test_files_path = os.path.join(os.path.dirname(__file__), 'testfiles')

@attr("slow", "template", "template_aft")
class ProjectTemplateCloneTest(unittest.TestCase):

	def setUp(self):
		test_utils.skip_if_group_failed_or_skipped("workspace_aft")
		self.project_template = ProjectTemplate()
		self.config = Config()

	def tearDown(self):
		pass
	
	def test_1_clone_if_current_project_not_set_works(self):
		self.project_template.clone_if_current_project_not_set()

	def test_2_checkout_project_from_cvs_works_for_second_user(self):
		test_utils.skip_if_test_case_failed_or_was_skipped(self.test_1_clone_if_current_project_not_set_works)
		if self.config.current_project_path is None:
			self.project_template.checkout_project_from_cvs("ptcvsuser2", "_copy");

	def test_2_create_sub_project_works(self):
		test_utils.skip_if_test_case_failed_or_was_skipped(self.test_1_clone_if_current_project_not_set_works)
		if self.config.current_project_path is None:
			self.project_template.create_sub_project()

@attr("unit", "template", "template_unit")
class ProjectTemplateUnitTest(unittest.TestCase):
	
	def setUp(self):
		self.config = Config(test_config_file_path)
		self.project_template = ProjectTemplate(config = self.config)

	def test_update_power_tools_xml(self):
		xml_file = os.path.join(test_files_path, 'xml/powertools.xml')
		self.project_template.update_power_tools_xml(pt_xml_path = xml_file)

	def test_update_power_tools_xml_works_with_sub_project(self):
		xml_file = os.path.join(test_files_path, 'xml/powertools.xml')
		self.project_template.update_power_tools_xml(
			pt_xml_path = xml_file
			, is_sub_project = True
		)

	def test_load_cvs_settings_from_current_project(self):
		
		#replace it with our own for testing
		self.config.current_project_path = test_files_path

		self.project_template.load_cvs_settings_from_current_project_path(sub_dir=".")

		self.assertEqual("ptcvsuser2", self.project_template.cvs_user)
		self.assertEqual("spibuild04.somecompany.net", self.project_template.cvs_server)
		self.assertEqual("/home/innovation/cvs2", self.project_template.cvs_repo)
		self.assertEqual("38707928-c95c-45c8-ab98-026cd85f591b", self.project_template.clone_name)

	def test_cvs_module_name(self):
		self.project_template.cvs_module_name()

	def test_cvs_url(self):
		self.project_template.cvs_url()

	def test_0_template_dir(self):
		self.assertIsNotNone(self.project_template.template_dir(), "Expcted CUSTDEMO_HOME to be set.")

	def test_dest_dir(self):
		test_utils.skip_if_test_case_failed_or_was_skipped(self.test_0_template_dir)
		self.project_template.dest_dir()

	def test_full_clone_path(self):
		test_utils.skip_if_test_case_failed_or_was_skipped(self.test_0_template_dir)
		self.project_template.full_clone_path()

	def test_working_dir(self):
		test_utils.skip_if_test_case_failed_or_was_skipped(self.test_0_template_dir)
		self.project_template.working_dir()

	def test_update_eclipse_project_file_works(self):
		project_file = os.path.join(test_files_path, 'xml/eclipse.project')
		self.project_template.update_eclipse_project_file(file_path = project_file)

	def test_delete_compiled_java_files_works(self):
		self.project_template.delete_compiled_java_files()


@attr("cleanup","template", "template_cleanup")
class ProjectTemplateCleanUpTest(unittest.TestCase):

	def setUp(self):
		self.shell = Shell()
		self.project_template = ProjectTemplate()
		self.environment_model = EnvironmentModel()
		self.powertools = PowerTools()
		self.powertools.close()


	def tearDown(self):
		pass

	def test_delete_all_clones_works(self):
		test_utils.skip_if_any_group_failed_or_skipped();
		self.project_template.delete_all_clones();
		#make sure the user folder has been deleted on the cvs server
		result = self.shell.execute("ssh " + self.project_template.cvs_server + " ls -la " + self.project_template.cvs_repo + nix_sep +  self.project_template.clones_folder)
		self.assertNotRegexpMatches(result, self.project_template.clones_folder + nix_sep + self.environment_model.current_username())
		#make sure the clone folder is still on the server
		result = self.shell.execute("ssh " + self.project_template.cvs_server + " ls -la " + self.project_template.cvs_repo)
		self.assertRegexpMatches(result, self.project_template.clones_folder)

