import unittest
import os
from os import path
import test_utils
from nose.plugins.attrib import attr

from backlog import Backlog, BacklogItem
from backlog_work import BacklogWork
from powertools import PowerTools
from attachment_template import AttachmentTemplates, AttachmentTemplate

powertools = PowerTools()

@attr("slow", "attachment_template", "attachment_template_aft")
class AttachmentTemplatesTest(unittest.TestCase):

	def setUp(self):
		test_utils.skip_if_group_failed_or_skipped("backlog_aft")
		powertools.focus()
		self.attachment_template = AttachmentTemplates()		
		self.backlog = Backlog()
		self.backlog_work = BacklogWork()
		self.template = AttachmentTemplate(
			 template_id = "Xunderwriting00064",
			 name = "Paint Chip",			
			 description = "Pant chip attachment",
			 comments = "Pait chip",
			 available_on = ["Quote", "Application", "Policy"]
		)
		self.backlog_item = BacklogItem(
			name = "Add attachment template",
	        item_type = "Advanced Configuration",
			estimate = "1",
			description = "Add attachment template",
			configurable_areas = ["Underwriting Attachment Templates"]
			
		)

	def tearDown(self):
		pass

	def test_that_1_add_backlog_item_works(self):
		self.backlog.add(self.backlog_item)

	def test_that_2_add_works(self):
		test_utils.skip_if_test_case_failed_or_was_skipped(self.test_that_1_add_backlog_item_works)
		self.attachment_template.add(self.template)

	def test_that_3_delete_works(self):
		test_utils.skip_if_test_case_failed_or_was_skipped(self.test_that_2_add_works)
		self.attachment_template.delete(self.template)

	def test_that_4_release_backlog_item_works(self):
		test_utils.skip_if_test_case_failed_or_was_skipped(self.test_that_3_delete_works)
		self.backlog_work.release_configurable_area(configurable_area = self.backlog_item.configurable_areas[0])

	def test_that_5_close_backlog_item_works(self):
		test_utils.skip_if_test_case_failed_or_was_skipped(self.test_that_4_release_backlog_item_works)
		self.backlog.close(self.backlog_item)

@attr("unit", "attachment_template", "attachment_template_unit")
class AttachmentTemplateUnitTest(unittest.TestCase):
	
	def setUp(self):
		test_dir = path.join(path.dirname(__file__), 'testfiles', 'xml')
		file_map = {
			"Quote":path.join(test_dir, 'quote', 'attachment.xml')
			, "Application":path.join(test_dir, 'app', 'attachment.xml')
			, "Policy":path.join(test_dir, 'policy', 'attachment.xml')
		}
		self.template = AttachmentTemplate(
			template_id = "Xunderwriting00064"
			, name = "Paint Chip"			
			, description = "Pant chip attachment"
			, available_on = ["Quote", "Application", "Policy"]
			, file_map = file_map
		)

	def tearDown(self):
		pass

	def test_that_verify_works(self):
		self.template.verify()

	def test_that_verify_deleted_works(self):
		self.template.name = "asdf"
		self.template.verify_deleted()
