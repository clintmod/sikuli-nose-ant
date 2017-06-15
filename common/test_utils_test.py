import os
import unittest
import test_utils
from nose.plugins.attrib import attr
from nose.tools import assert_equal
from nose.tools import raises

test_dependency_graph = {
	"search":{"unit"},
	"installer_aft":{"search"},
	"powertools_aft":{"installer_aft"},
	"workspace_aft":{"powertools_aft"},
	"template_aft":{"workspace_aft"},
	"project_aft":{"template_aft"},
	"backlog_aft": {"project_aft"},
	"backlog_work_aft": {"backlog_aft"},
	"common_authority_aft":{"backlog_work_aft"},
	"task_groups_aft":{"backlog_work_aft"},
	"task_templates_aft":{"backlog_work_aft"},
	"aft":{
		"common_authority_aft"
		, "task_groups_aft"
		, "task_templates_aft"
	},
	"project_cleanup":{"aft"},
	"template_cleanup":{"project_cleanup"}
}

@attr("unit", "test_utils", "test_utils_module_level")
class TestUtilsModuleLevelTest(unittest.TestCase):

	def setUp(self):
		self.original_results = test_utils.group_results
		test_utils.group_results = {}
 
	def tearDown(self):
		test_utils.group_results = self.original_results

	def test_add_group_result_works(self):
		test_utils.add_group_result("some_test_group", test_utils.FAILED)
		assert_equal(test_utils.group_results["some_test_group"], "failed")
		
	@raises(unittest.case.SkipTest)
	def test_skip_if_group_failed_or_skipped_works_with_failed(self):
		test_utils.add_group_result("some_test_group", test_utils.FAILED)
		test_utils.skip_if_group_failed_or_skipped("some_test_group")
		
	@raises(unittest.case.SkipTest)
	def test_skip_if_group_failed_or_skipped_works_with_skip(self):
		test_utils.add_group_result("some_test_group", test_utils.SKIPPED)
		test_utils.skip_if_group_failed_or_skipped("some_test_group")
	
	@raises(unittest.case.SkipTest)
	def test_skip_if_any_group_failed_works(self):
		test_utils.add_group_result("some_test_group", test_utils.FAILED)
		test_utils.skip_if_any_group_failed()
	@raises(unittest.case.SkipTest)
	def test_skip_if_any_group_failed_or_skipped_works_with_skip(self):
		test_utils.add_group_result("some_test_group", test_utils.SKIPPED)
		test_utils.skip_if_any_group_failed_or_skipped()

	@raises(unittest.case.SkipTest)
	def test_skip_if_any_group_failed_or_skipped_works_with_failed(self):
		test_utils.add_group_result("some_test_group", test_utils.FAILED)
		test_utils.skip_if_any_group_failed_or_skipped()
		
	def test_skip_if_group_failed_or_skipped_works_when_called_with_successful_group(self):
		test_utils.skip_if_group_failed_or_skipped("some_test_group_not_in_results")


@attr("unit", "test_utils")
class TestUtilsTest(unittest.TestCase):
	
	def setUp(self):
		test_utils.default_test_dependency_graph = test_dependency_graph
 
	def tearDown(self):
		pass

	def test_get_ordered_test_groups_works(self):
		expected = ("unit,search,installer_aft,powertools_aft,workspace_aft,template_aft"
			+ ",project_aft,backlog_aft,backlog_work_aft,common_authority_aft"
			+ ",task_groups_aft,task_templates_aft,aft,project_cleanup,template_cleanup")
		result = test_utils.get_ordered_test_groups(test_dependency_graph)
		actual = ",".join(result)
		self.assertEquals(expected, actual)

@attr("unit", "test_utils", "test_runner")
class TestRunnerParserTest(unittest.TestCase):

	def setUp(self):
		self.runner = test_utils.TestRunner()
		self.expected_reports_dir = "asdf"
		self.expected_working_dir = "ohya"
		self.args = [
			"-reports-dir=" + self.expected_reports_dir,
			"-working-dir=" + self.expected_working_dir
		]

	def test_parse_works(self):
		expected = ""
		self.runner.parse(self.args)

	def test_parse_works_with_modules(self):
		self.assertEqual(0, len(self.runner.modules))
		self.args.append("-modules=asdf/utils.py,asdf/utils2.py")
		expected = "asdf/utils.py,asdf/utils2.py"
		self.runner.parse(self.args)
		self.assertEquals(expected, ",".join(self.runner.modules))

	def test_parse_works_with_one_module(self):
		self.args.append("-modules=asdf/utils.py")
		expected = "asdf/utils.py"
		self.runner.parse(self.args)
		self.assertEquals(expected, ",".join(self.runner.modules))
		
	def test_parse_works_with_groups(self):
		self.assertEqual(0, len(self.runner.groups))
		self.args.append("-groups=unit,powertools")
		expected = "unit,powertools"
		self.runner.parse(self.args)
		self.assertEquals(expected, ",".join(self.runner.groups))

	def test_parse_works_with_one_group(self):
		self.args.append("-groups=unit")
		expected = "unit"
		self.runner.parse(self.args)
		self.assertEquals(expected, ",".join(self.runner.groups))

	def test_parse_works_with_default_groups(self):
		expected = ",".join(test_utils.get_ordered_test_groups())
		self.runner.parse(self.args)
		self.assertEquals(expected, ",".join(self.runner.groups))

	def test_parse_works_with_ids(self):
		self.assertEqual(0, len(self.runner.ids))
		self.args.append("-ids=1,2")
		expected = "1,2"
		self.runner.parse(self.args)
		self.assertEquals(expected, ",".join(self.runner.ids))

	def test_parse_works_with_one_id(self):
		self.args.append("-ids=1")
		expected = "1"
		self.runner.parse(self.args)
		self.assertEquals(expected, ",".join(self.runner.ids))

	def test_parse_works_with_reports_dir(self):
		self.assertEqual("", self.runner.reports_dir)
		self.runner.parse(self.args)
		self.assertEqual(self.expected_reports_dir, self.runner.reports_dir)

	def test_parse_works_with_fail_only(self):
		self.assertEqual(False, self.runner.fail_only)
		self.args.append("-fail-only=1")
		self.runner.parse(self.args)
		self.assertEqual(True,self.runner.fail_only)

	def test_parse_works_with_collect_only(self):
		self.assertEqual(False, self.runner.collect_only)
		self.args.append("-collect-only=1")
		self.runner.parse(self.args)
		self.assertEqual(True,self.runner.collect_only)

@attr("unit", "test_utils", "test_runner")
class TestRunnerTest(unittest.TestCase):

	def setUp(self):
		self.runner = test_utils.TestRunner()
		self.expected_reports_dir = "reports/aft"
		self.expected_working_dir = "."
		self.args = [
			"-reports-dir=" + self.expected_reports_dir,
			"-working-dir=" + self.expected_working_dir
 		]

	def test_convert_to_nose_args_works(self):
		self.runner.parse(self.args)
		expected = ",".join(self.runner.default_nose_args())
		actual = ",".join(self.runner.convert_to_nose_args())
		self.assertEqual(expected, actual)

	def test_convert_to_nose_args_returns_dummy_first_arg(self):
		self.runner.parse(self.args)
		actual = self.runner.convert_to_nose_args()
		self.assertTrue("dummy" in actual[0])

	def test_convert_to_nose_args_works_with_a_group(self):
		group = "unit"
		self.args.append("-groups="+group)
		self.runner.parse(self.args)

		default_nose_args = self.runner.default_nose_args()
		default_nose_args.append("-a " + group)
		default_nose_args.append("--with-xunit")
		default_nose_args.append("--xunit-file")
		default_nose_args.append(self.runner.reports_dir+"/"+group+".xml")
		expected = ",".join(default_nose_args)
		
		actual = ",".join(self.runner.convert_to_nose_args(group))
		self.assertEqual(expected, actual)


	def test_convert_to_nose_args_works_with_a_module(self):
		module = "common/utils.py"
		self.args.append("-modules="+module)
		self.runner.parse(self.args)

		default_nose_args = self.runner.default_nose_args()
		default_nose_args.append(module)
		expected = ",".join(default_nose_args)
		
		actual = ",".join(self.runner.convert_to_nose_args())
		self.assertEqual(expected, actual)

	def test_convert_to_nose_args_works_with_modules(self):
		modules = ["common/utils.py","common/installer.py"]
		self.args.append("-modules="+",".join(modules))
		self.runner.parse(self.args)

		default_nose_args = self.runner.default_nose_args()
		for index, module in enumerate(modules):
			default_nose_args.append(module)

		expected = ",".join(default_nose_args)
		
		actual = ",".join(self.runner.convert_to_nose_args())
		self.assertEqual(expected, actual)


	def test_convert_to_nose_args_works_with_an_id(self):
		id_ = "54"
		self.args.append("-ids="+id_)
		self.runner.parse(self.args)

		default_nose_args = self.runner.default_nose_args()
		default_nose_args.insert(self.runner.id_index+1, id_)
		expected = ",".join(default_nose_args)
		
		actual = ",".join(self.runner.convert_to_nose_args())
		self.assertEqual(expected, actual)

	def test_convert_to_nose_args_works_with_ids(self):
		ids = ["1","2"]
		self.args.append("-ids="+",".join(ids))
		self.runner.parse(self.args)

		default_nose_args = self.runner.default_nose_args()
		for index, id_ in enumerate(ids):
			new_id = self.runner.id_index + 1 + index
			default_nose_args.insert(new_id, id_)

		expected = ",".join(default_nose_args)
		
		actual = ",".join(self.runner.convert_to_nose_args())
		self.assertEqual(expected, actual)

	def test_convert_to_nose_args_works_with_a_fail_only(self):
		self.args.append("-fail-only")
		self.runner.parse(self.args)

		default_nose_args = self.runner.default_nose_args()
		default_nose_args.append("--failed")
		expected = ",".join(default_nose_args)
		
		actual = ",".join(self.runner.convert_to_nose_args())
		self.assertEqual(expected, actual)

	def test_convert_to_nose_args_works_with_a_collect_only(self):
		self.args.append("-collect-only")
		self.runner.parse(self.args)

		default_nose_args = self.runner.default_nose_args()
		default_nose_args.append("--collect-only")
		expected = ",".join(default_nose_args)
		
		actual = ",".join(self.runner.convert_to_nose_args())
		self.assertEqual(expected, actual)
