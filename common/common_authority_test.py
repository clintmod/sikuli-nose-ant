import unittest
import os
import test_utils
from nose.plugins.attrib import attr

from backlog import Backlog, BacklogItem
from backlog_work import BacklogWork
from common_authority import CommonAuthority, AuthorityAttribute, AuthorityRole
from powertools import PowerTools

powertools = PowerTools()

item = BacklogItem(
	name = "Add Dune Buggy",
	item_type = "Advanced Configuration",
	estimate = "1",
	description = "Support Dune Buggies",
	configurable_areas = ["Common Authority"]
)

role = AuthorityRole(
	uid = "JuniorPolicyAgent",
	name = "Junior Policy Agent",
	description = "Junior Policy Agent",
	area = "Policy"
)

expected_set = '<AuthorityAttribute id="AllowToApproveDuneBuggy" Name="Allow To Approve Dune Buggy" Description="Allow To Approve Dune Buggy" DataTypeCd="YesNo" DefaultValue="No" />'

@attr("slow", "common_authority", "common_authority_aft")
class CommonAuthorityAddAttributeTest(unittest.TestCase):

	def setUp(self):
		test_utils.skip_if_group_failed_or_skipped("backlog_aft")
		powertools.focus()
		self.common_authority = CommonAuthority()
		self.backlog = Backlog()
		self.backlog_work = BacklogWork()
		self.attrib = AuthorityAttribute(
			attribute_id = "AllowToApproveDuneBuggy",
			name = "Allow To Approve Dune Buggy",
			description = "Allow To Approve Dune Buggy",
			default_value = "No",
			data_type = "YesNo",
			authority_set = "Policy Approvals",
			role_permissions = [
				("Policy Agent", "No"),
				("Policy Underwriter", "Yes")
			],
		)

	def tearDown(self):
		pass

	def test_that_1_add_backlog_item_works(self):
		self.backlog.add(item)

	def test_that_2_0_add_attribute_works(self):
		test_utils.skip_if_test_case_failed_or_was_skipped(self.test_that_1_add_backlog_item_works)
		self.common_authority.add_attribute(self.attrib)

	def test_that_2_1_set_role_permissions_work(self):
		test_utils.skip_if_test_case_failed_or_was_skipped(self.test_that_2_0_add_attribute_works)
		self.common_authority.set_role_permissions(self.attrib)

	def test_that_2_2_copy_role_works(self):
		test_utils.skip_if_test_case_failed_or_was_skipped(self.test_that_2_0_add_attribute_works)
		self.common_authority.copy_role("Policy Agent", role)

	def test_that_3_delete_attribute_works(self):
		test_utils.skip_if_test_case_failed_or_was_skipped(self.test_that_2_1_set_role_permissions_work)
		self.common_authority.delete_attribute(self.attrib)

	def test_that_4_release_backlog_item_works(self):
		test_utils.skip_if_test_case_failed_or_was_skipped(self.test_that_3_delete_attribute_works)
		self.backlog_work.release_configurable_area(configurable_area = "Common Authority")

	def test_that_5_close_backlog_item_works(self):
		test_utils.skip_if_test_case_failed_or_was_skipped(self.test_that_4_release_backlog_item_works)
		self.backlog.close(item)


@attr("unit", "common_authority", "common_authority_unit")
class AuthorityAttributeTest(unittest.TestCase):
	
	def setUp(self):
		self.attrib = AuthorityAttribute(
			file_path = os.path.join(os.path.dirname(__file__), 'testfiles', 'xml', 'authority-set.xml'),
			attribute_id = "AllowToApproveDuneBuggy",
			name = "Allow To Approve Dune Buggy",
			description = "Allow To Approve Dune Buggy",
			default_value = "No",
			data_type = "YesNo",
			authority_set = "Policy Approvals",
			role_permissions = [
				("Policy Agent", "No"),
				("Policy Underwriter", "Yes")
			],
		)
		self.role = AuthorityRole(
			uid = "asdf1",
			name = "asdf2",
			description = "asdf3",
			area = "asdf4"
		)

	def tearDown(self):
		pass

	def test_that_constructor_works(self):
		self.assertEqual("AllowToApproveDuneBuggy", self.attrib.id)
		self.assertEqual("Allow To Approve Dune Buggy", self.attrib.name)
		self.assertEqual("Allow To Approve Dune Buggy", self.attrib.description)
		self.assertEqual("No", self.attrib.default_value)
		self.assertEqual("YesNo", self.attrib.data_type)
		self.assertEqual("Policy Approvals", self.attrib.authority_set)
		self.assertIsNotNone(self.attrib.role_permissions)

		self.assertEqual("asdf1", self.role.uid)
		self.assertEqual("asdf2", self.role.name)
		self.assertEqual("asdf3", self.role.description)
		self.assertEqual("asdf4", self.role.area)

	def test_that_to_xml_works(self):
		expected = '<AuthorityAttribute id="AllowToApproveDuneBuggy" Name="Allow To Approve Dune Buggy" Description="Allow To Approve Dune Buggy" DataTypeCd="YesNo" DefaultValue="No" />'
		actual = self.attrib.to_xml()
		self.assertEqual(expected,actual)

	def test_that_verify_authority_set_works(self):
		self.attrib.verify_authority_set()
