import nose
from nose.plugins import Plugin
from nose.exc import SkipTest
from common import test_utils

class LiveResult(Plugin):

	name = 'live-results'
	enabled = True

	def afterTest(self, test):
		result = test.test._resultForDoCleanups
		if result is not None:
			test_utils.live_result = result
		