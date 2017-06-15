import os
import unittest
import backlog_test
import test_utils
from backlog_work import BacklogWork
from backlog import Backlog
from powertools import PowerTools
from nose.plugins.attrib import attr

powertools = PowerTools()

@attr("slow", "backlog_work", "backlog_work_dev")
class BacklogWorkDevTest(unittest.TestCase):
	def setUp(self):
		self.backlog_work = BacklogWork()
		powertools.focus()
			
	def tearDown(self):
		pass

	def test_that_release_configurable_area_works(self):
		self.backlog_work.release_configurable_area('Underwriting Note Templates')

@attr("slow", "backlog_work", "backlog_work_aft")
class BacklogWorkTest(unittest.TestCase):

	def setUp(self):
		test_utils.skip_if_group_failed_or_skipped("backlog_aft")
		self.backlog_work = BacklogWork()
		powertools.focus()
			
	def tearDown(self):
		pass

	def test_that_undo_work_item_works(self):
		self.backlog_work.undo_work_item(backlog_test.item)

