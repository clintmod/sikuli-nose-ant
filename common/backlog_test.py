import os
import unittest
import test_utils
from sikuli import *
from common import PowerTools
from common_authority import AuthorityAttribute

from backlog import Backlog, BacklogItem
from nose.plugins.attrib import attr

powertools = PowerTools()

item = BacklogItem(
	name = "Add Dune Buggy",
	item_type = "Advanced Configuration",
	estimate = "1",
	description = "Support Dune Buggies",
	configurable_areas = ["Common Authority", "Pay Plans"]
)

@attr("unit", "backlog", "backlog_unit")
class BacklogItemUnitTest(unittest.TestCase):
	
	def setUp(self):
		pass
			
	def tearDown(self):
		pass

	def test_that_constructor_works(self):
		item = BacklogItem(
			name = "asdf1",
			owner = "asdf2",
			item_type = "asdf3",
			estimate = "asdf4",
			description = "asdf5",
			configurable_areas = ["asdf6", "Policy Approvals"]
		)
		self.assertEquals("asdf1", item.name)
		self.assertEquals("asdf2", item.owner)
		self.assertEquals("asdf3", item.type)
		self.assertEquals("asdf4", item.estimate)
		self.assertEquals("asdf5", item.description)
		self.assertEquals("asdf6", item.configurable_areas[0])
		self.assertEquals("Policy Approvals", item.configurable_areas[1])

@attr("slow", "backlog", "backlog_aft")
class BacklogItemTest(unittest.TestCase):
	
	def setUp(self):
		test_utils.skip_if_group_failed_or_skipped("project_aft")
		self.backlog = Backlog()
		powertools.focus()
	
	def tearDown(self):
		pass

	def test_that_1_add_works(self):
		print "getAutoWaitTimeout " + str(getAutoWaitTimeout())
		self.backlog.add(item)

	def test_that_2_close_works(self):
		test_utils.skip_if_test_case_failed_or_was_skipped(self.test_that_1_add_works)
		self.backlog.close(item)