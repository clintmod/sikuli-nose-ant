import os
import unittest
import graph_utils
import shutil
import nose
from utils import ScreenUtils
from time import sleep

previous_test_result = None

live_result = None

group_results = {}

SKIPPED = "skipped"
FAILED = "failed"

#presumes powertools is opened to a new project
dev_test_dependency_graph = {
	"backlog_work_aft": {"backlog_aft"}
	,"common_authority_aft":{"backlog_work_aft"}
	,"task_groups_aft":{"backlog_work_aft"}
	,"task_templates_aft":{"backlog_work_aft"}
	,"note_templates_aft":{"backlog_work_aft"}
}

default_test_dependency_graph = {
	"unit":{"test_utils"}
	,"search_aft":{"unit"}
	,"scroller_aft":{"search_aft"}
	,"installer_aft":{"scroller_aft"}
	,"powertools_aft":{"installer_aft"}
	,"workspace_aft":{"powertools_aft"}
	,"template_aft":{"workspace_aft"}
	,"project_aft":{"template_aft"}
	,"backlog_aft": {"project_aft"}
	,"backlog_work_aft": {"backlog_aft"}
	,"common_authority_aft":{"backlog_work_aft"}
	,"task_groups_aft":{"backlog_work_aft"}
	,"task_templates_aft":{"backlog_work_aft"}
	,"note_templates_aft":{"backlog_work_aft"}
	, "attachment_template_aft":{"backlog_work_aft"}
	,"all_afts":{
		"common_authority_aft"
		, "task_groups_aft"
		, "attachment_template_aft"
		, "task_templates_aft"
		, "note_templates_aft"
	}
	,"project_cleanup":{"all_afts"}
	,"template_cleanup":{"project_cleanup"}
	,"aft_artifact_archival":{"template_cleanup"}
	,"installer_cleanup":{"aft_artifact_archival"}
}

def skip_if_test_cases_failed_or_were_skipped(test_cases = []):
	'''
	This method only works for methods contained in the same module
	'''
	for test_case in test_cases:
		skip_if_test_case_failed_or_skipped(test_case)

def skip_if_test_case_failed_or_was_skipped(test_case):
	'''
	This method only works for methods contained in the same module
	'''
	if live_result is None: #first test
		return
	test_name = test_case.__name__
	print str(live_result.skipped)
	if test_name in str(live_result.skipped):
		raise unittest.case.SkipTest("Skipped because " + test_name + " was skipped ")
	if(test_name in str(live_result.errors) or 
	   test_name in str(live_result.failures)):
		raise unittest.case.SkipTest("Skipped because " + test_name + " failed ")
		

def skip_if_groups_failed_or_skipped(groups = []):
	if isinstance(groups, list):
		for group in groups:
			skip_if_group_failed_or_skipped(group)

def skip_if_group_failed_or_skipped(group = ""):
	result = group_results.get(group)
	if result == FAILED or result == SKIPPED:
		raise unittest.case.SkipTest('Skipped because the group ' + group + ' failed or was skipped.')

def skip_if_any_group_failed():
	for group in group_results:
		if group_results.get(group) == FAILED:
			raise unittest.case.SkipTest('Skipped because the group ' + group + ' failed or was skipped.')

def skip_if_any_group_failed_or_skipped():
	for group in group_results:
		if group_results.get(group) == FAILED or group_results.get(group) == SKIPPED:
			raise unittest.case.SkipTest('Skipped because the group ' + group + ' failed or was skipped.')

def add_group_result(group, result):
	group_results[group] = result

def get_ordered_test_groups(graph = None):
	graph = graph or default_test_dependency_graph
	return graph_utils.topology_sort_flatten(graph)

class Totals(object):
	def __init__(self):
		self.results = []
		self.init_vals()

	def init_vals(self):
		self.testsRun = 0
		self.errors = 0
		self.failures = 0
		self.skipped = 0

	def tally(self):
		self.init_vals()
		for result in self.results:
			self.testsRun += result.testsRun
			self.errors += len(result.errors)
			self.failures += len(result.failures)
			self.skipped += len(result.skipped)
	
	def print_summary(self):
		self.tally()
		print "\nSummary - run: {0}, errors: {1}, failures: {2}, skipped: {3}\n".format(
			self.testsRun, self.errors, self.failures, self.skipped)

class TestRunner(object):
	
	def __init__(self):
		self.init_values()
		self.screen_utils = ScreenUtils()

	def init_values(self):
		self.working_dir = ""
		self.reports_dir = ""
		self.groups = []
		self.modules = []
		self.ids = []
		self.fail_only = False
		self.collect_only = False
		self.verbosity = 2
		self.xunit = True
		self.xunit_file = ""
		self.screen_capture = True
		self.parse_was_called = False
		self.id_index = 1

	def parse(self, args):
		self.init_values()
		self.parse_was_called = True
		args = args or []
		for index, arg in enumerate(args):
			if "-groups=" in arg:
				groups_csv_string = arg.replace("-groups=", "")
				if groups_csv_string != "":
					self.groups = groups_csv_string.split(",")
			elif "-modules=" in arg:
				modules_csv_string = arg.replace("-modules=", "")
				if modules_csv_string != "":
					self.modules = modules_csv_string.split(",")
			elif "-ids=" in arg:
				ids_csv_string = arg.replace("-ids=", "")
				if ids_csv_string != "":
					self.ids = ids_csv_string.split(",")
			elif "-reports-dir=" in arg:
				self.reports_dir = arg.split("=")[1]
			elif "-fail-only" in arg:
				self.fail_only = True
			elif "-collect-only" in arg:
				self.collect_only = True
			elif "-working-dir" in arg:
				self.working_dir = arg.split("=")[1]
			elif "-verbosity=" in arg:
				self.verbosity = arg.split("=")[1]
			elif "-no-xunit" in arg:
				self.xunit = False

		#use default groups if we found zero groups
		if len(self.groups) == 0:
			self.groups = get_ordered_test_groups()

		if self.reports_dir == "":
			raise ValueError("expected -reports-dir argument")

		if self.working_dir == "":
			raise ValueError("expected -working-dir argument")

		return self

	def default_nose_args(self):
		return_val = [
			" dummy arg",
			"--verbosity={0}".format(self.verbosity),
			"--with-screen-capture",
			"--with-live-results",
		]
		return_val.insert(self.id_index, "--with-id")
		return_val.append("-w")
		return_val.append(self.working_dir)
		return return_val

	def convert_to_nose_args(self, group = None):
		if not self.parse_was_called:
			raise Exception("you need to call parse(args) first")
		return_val = self.default_nose_args()
		if(group is not None):
			return_val.append("-a " + group)
			if self.xunit:
				return_val.append("--with-xunit")
				return_val.append("--xunit-file")
				return_val.append(self.reports_dir+"/"+group+".xml")
		for module in self.modules:
			return_val.append(module)
		for index, id_ in enumerate(self.ids):
			new_index = self.id_index + 1 + index
			return_val.insert(new_index, id_) 
		if self.fail_only:
			return_val.append("--failed")
		if self.collect_only:
			return_val.append("--collect-only")
		return return_val

	def execute(self):
		self.clean_and_create_reports_dir()
		totals = Totals()
		if self.fail_only or len(self.ids) > 0:
			group = self.groups[0] if len(self.groups) ==1 else None
			self.run_nose(group)
		else:
			for group in self.groups:
				test_program = self.run_nose(group)
				global previous_test_result
				previous_test_result = test_program.result
				totals.results.append(previous_test_result)
				if (not test_program.success):
					print "\nadding group failure: " + group
					add_group_result(group , FAILED)
				if len(previous_test_result.skipped) > 0:
					add_group_result(group, SKIPPED)
			sleep(0.3)
			if len(totals.results) > 1:
				totals.print_summary()

	def run_nose(self, group):
		if "_aft" in group:
			self.screen_utils.start_video_capture(output_file_name = group)
		nose_args = self.convert_to_nose_args(group = group)
		test_progam = nose.main(argv = nose_args, exit=False)
		if "_aft" in group:
			self.screen_utils.stop_video_capture()
			sleep(0.5)
		return test_progam

	def clean_and_create_reports_dir(self,reports_dir = None):
		reports_dir = reports_dir or self.reports_dir
		if os.path.exists(reports_dir):
			shutil.rmtree(reports_dir)
		os.makedirs(reports_dir)