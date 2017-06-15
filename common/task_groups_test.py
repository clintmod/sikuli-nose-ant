import unittest
import os
import test_utils
from nose.plugins.attrib import attr

from backlog import Backlog, BacklogItem
from backlog_work import BacklogWork
from powertools import PowerTools
from task_groups import TaskGroups, TaskGroup

powertools = PowerTools()

item = BacklogItem(
	name = "Paint Chip Review",
	item_type = "Advanced Configuration",
	estimate = "1",
	description = "Paint Chip Review",
	configurable_areas = [
		"Underwriting Task Groups"
	]
)

@attr("slow", "task_groups", "task_groups_aft")
class TaskGroupCopyTest(unittest.TestCase):

	def setUp(self):
		test_utils.skip_if_group_failed_or_skipped("backlog_aft")
		powertools.focus()
		self.task_groups = TaskGroups()
		self.backlog = Backlog()
		self.backlog_work = BacklogWork()
		self.group = TaskGroup(
			group_id = "PaintChipReview"
			, name = "Paint Chip Review"
			, description = "Task Group to do Paint Chip Review"
			, task_group_resolver_name = "Select..."
			, deactivation_date = None
			, escalate_to = "Select..."
			, copied_from = "Underwriting"
		)

	def tearDown(self):
		pass

	def test_that_1_add_backlog_item_works(self):
		self.backlog.add(item)

	def test_that_2_0_copy_works(self):
		test_utils.skip_if_test_case_failed_or_was_skipped(self.test_that_1_add_backlog_item_works)
		self.task_groups.copy(self.group)

	def test_that_3_delete_works(self):
		test_utils.skip_if_test_case_failed_or_was_skipped(self.test_that_2_0_copy_works)
		self.task_groups.delete(self.group)

	def test_that_4_release_backlog_item_works(self):
		test_utils.skip_if_test_case_failed_or_was_skipped(self.test_that_3_delete_works)
		self.backlog_work.release_configurable_area(configurable_area = item.configurable_areas[0])

	def test_that_5_close_backlog_item_works(self):
		test_utils.skip_if_test_case_failed_or_was_skipped(self.test_that_4_release_backlog_item_works)
		self.backlog.close(item)


@attr("unit", "task_groups", "task_groups_unit")
class TaskGroupUnitTest(unittest.TestCase):
	
	def setUp(self):
		test_file = os.path.join(os.path.dirname(__file__), 'testfiles', 'xml', 'task-group.xml')
		task_group_rules_file_path = os.path.join(os.path.dirname(__file__), 'testfiles', 'xml', 'task-group-rules.xml')
		self.task_group = TaskGroup(
			file_path = test_file
			, task_group_rules_file_path = task_group_rules_file_path
			, group_id = "PaintChipReview"
			, name = "Paint Chip Review"
			, description = "Task Group to do Paint Chip Review"
			, task_group_resolver_name = "Producer"
			, deactivation_date = None
			, escalate_to = "Select..."
			, copied_from = "Producer"
		)

	def tearDown(self):
		pass

	def test_that_to_xml_works(self):
		self.task_group.to_xml()

	def test_that_verify_works(self):
		self.task_group.verify()

	def test_that_load_from_copy_works(self):
		self.task_group.load_from_copy()

	def test_that_get_task_group_resolver_class_works(self):
		expected = "com.somecompany.uw.policy.PolicyTask"
		actual = self.task_group.get_task_group_resolver_class("Producer")
		self.assertEqual(expected, actual)