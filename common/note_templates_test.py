import unittest
import os
from os import path
import test_utils
from nose.plugins.attrib import attr

from backlog import Backlog, BacklogItem
from backlog_work import BacklogWork
from powertools import PowerTools
from note_templates import NoteTemplates, NoteTemplate

powertools = PowerTools()

@attr("slow", "note_templates", "note_templates_dev")
class NoteTemplateDevTest(unittest.TestCase):

	def setUp(self):
		powertools.focus()
		self.note_templates = NoteTemplates()

@attr("slow", "note_templates", "note_templates_aft")
class NoteTemplateAddTest(unittest.TestCase):

	def setUp(self):
		test_utils.skip_if_group_failed_or_skipped("backlog_aft")
		powertools.focus()
		self.note_templates = NoteTemplates()
		self.backlog = Backlog()
		self.backlog_work = BacklogWork()
		self.template = NoteTemplate(
			name = "1 Agent Note Name"
			, copy_from = {'name':"Agent Note", 'package':"Policy"}
			, description = "1 Agent Note Description"
			, available_on = ["Quote", "Application", "Policy"]
		)
		self.backlog_item = BacklogItem(
			name = "Notes 1"
			, item_type = "Advanced Configuration"
			, estimate = "1"
			, description = "Notes 2"
			, configurable_areas = [
				"Underwriting Note Templates"
			]
		)

	def tearDown(self):
		pass

	def test_that_1_add_backlog_item_works(self):
		self.backlog.add(self.backlog_item)

	def test_that_2_add_works(self):
		test_utils.skip_if_test_case_failed_or_was_skipped(self.test_that_1_add_backlog_item_works)
		self.note_templates.add(self.template)

	def test_that_3_delete_works(self):
		test_utils.skip_if_test_case_failed_or_was_skipped(self.test_that_2_add_works)
		self.note_templates.delete(self.template)

	def test_that_4_release_backlog_item_works(self):
		test_utils.skip_if_test_case_failed_or_was_skipped(self.test_that_3_delete_works)
		self.backlog_work.release_configurable_area(configurable_area = self.backlog_item.configurable_areas[0])

	def test_that_5_close_backlog_item_works(self):
		test_utils.skip_if_test_case_failed_or_was_skipped(self.test_that_4_release_backlog_item_works)
		self.backlog.close(self.backlog_item)


@attr("unit", "note_templates", "note_templates_unit")
class NoteTemplateUnitTest(unittest.TestCase):
	
	def setUp(self):
		test_dir = path.join(path.dirname(__file__), 'testfiles', 'xml')
		file_map = {
			"Quote":path.join(test_dir, 'quote-note.xml')
			, "Application":path.join(test_dir, 'app-note.xml')
			, "Policy":path.join(test_dir, 'policy-note.xml')
		}
		self.template = NoteTemplate(
			name = "1 Agent Note Name"
			, copy_from = {'name':"Agent Note", 'package':"Policy"}
			, description = "1 Agent Note Description"
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
