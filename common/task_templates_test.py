import unittest
import os
import test_utils
from nose.plugins.attrib import attr

from backlog import Backlog, BacklogItem
from backlog_work import BacklogWork
from powertools import PowerTools
from task_templates import TaskTemplates, TaskTemplate

powertools = PowerTools()


@attr("slow", "task_templates", "task_templates_dev")
class TaskTemplateDevTest(unittest.TestCase):

	def setUp(self):
		powertools.focus()
		self.task_templates = TaskTemplates()

	def test_that_check_checkbox_if_unchecked_works(self):
		self.task_templates.check_checkbox_if_unchecked(label = "Work Required")
		self.task_templates.check_checkbox_if_unchecked(label = "Work Required")

@attr("slow", "task_templates", "task_templates_aft")
class TaskTemplateAddTest(unittest.TestCase):

	def setUp(self):
		test_utils.skip_if_group_failed_or_skipped("backlog_aft")
		powertools.focus()
		self.task_templates = TaskTemplates()
		self.backlog = Backlog()
		self.backlog_work = BacklogWork()
		self.template = TaskTemplate(
			template_id = "1 ObtainPaintChip ID"
			, name = "1 Obtain Paint Chip Name"
			, task_type = "Manual"
			, text = "1 Obtain Paint Chip Text"
			, description = "Obtain Paint Chip Description"
			, work_required = True
			, show_in_inbox = True
			, assignment_owner_type = "User"
			, package = "Quote"
		)
		self.backlog_item = BacklogItem(
			name = "Obtain a Paint Chip",
			item_type = "Advanced Configuration",
			estimate = "1",
			description = "Obtain a Paint Chip",
			configurable_areas = [
				"Underwriting Task Templates"
			]
		)

	def tearDown(self):
		pass

	def test_that_1_add_backlog_item_works(self):
		self.backlog.add(self.backlog_item)

	def test_that_2_add_works(self):
		test_utils.skip_if_test_case_failed_or_was_skipped(self.test_that_1_add_backlog_item_works)
		self.task_templates.add(self.template)

	def test_that_3_delete_works(self):
		test_utils.skip_if_test_case_failed_or_was_skipped(self.test_that_2_add_works)
		self.task_templates.delete(self.template)

	def test_that_4_release_backlog_item_works(self):
		test_utils.skip_if_test_case_failed_or_was_skipped(self.test_that_3_delete_works)
		self.backlog_work.release_configurable_area(configurable_area = self.backlog_item.configurable_areas[0])

	def test_that_5_close_backlog_item_works(self):
		test_utils.skip_if_test_case_failed_or_was_skipped(self.test_that_4_release_backlog_item_works)
		self.backlog.close(self.backlog_item)


@attr("unit", "task_templates", "task_templates_unit")
class TaskTemplateUnitTest(unittest.TestCase):
	
	def setUp(self):
		test_file = os.path.join(os.path.dirname(__file__), 'testfiles', 'xml', 'task.xml')
		self.template = TaskTemplate(
			file_path = test_file
			, template_id = "1 ObtainPaintChip ID"
			, name = "1 Obtain Paint Chip Name"
			, task_type = "Manual"
			, text = "1 Obtain Paint Chip Text"
			, description = "Obtain Paint Chip Description"
			, work_required = True
			, show_in_inbox = True
			, assignment_owner_type = "User"
			, package = "Quote"
		)

	def tearDown(self):
		pass

	def test_that_verify_works(self):
		self.template.verify()

	def test_that_verify_deleted_works(self):
		self.template.name = "asdf"
		self.template.verify_deleted()
