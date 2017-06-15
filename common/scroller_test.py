from sikuli import *
import os
import unittest
import test_utils
import scroller
from scroller import Scroller, TimeoutException, ScrollTimeOutTimer, ScrollThumbNotFoundException
from nose.plugins.attrib import attr
from nose.tools import raises
from search import flex_label

app = None

@attr("unit", "scroller", "scroller_unit")
class ScrollerUnitTest(unittest.TestCase):

	def setUp(self):
		self.scroller = Scroller()
	
	def tearDown(self):
		pass

	@raises(ValueError)
	def test_get_scroll_to_location_handles_null(self):
		self.scroller.get_scroll_to_location(None, None)

	@raises(ValueError)
	def test_get_scroll_to_location_handles_null_region(self):
		self.scroller.get_scroll_to_location(None, scroller.HORIZONTAL)

	def test_get_scroll_to_location_works_when_horiztonal(self):
		region = Region(3,4,5,6)
		location = self.scroller.get_scroll_to_location(region, scroller.HORIZONTAL, 100)
		self.assertEqual(103, location.x)

	def test_get_scroll_to_location_works_when_vertical(self):
		region = Region(3,4,5,6)
		location = self.scroller.get_scroll_to_location(region, scroller.VERTICAL, 100)
		self.assertEqual(104, location.y)


@attr("unit", "scroller", "scroller_timeout")
class ScrollTimeOutTimerUnitTest(unittest.TestCase):

	def setUp(self):
		self.timer = ScrollTimeOutTimer(2,1)
	
	def tearDown(self):
		pass

	def test_timed_out_works(self):
		self.assertTrue(self.timer.timed_out(3))

	def test_timed_out_works_when_not_timed_out(self):
		self.assertFalse(self.timer.timed_out(1))

@attr("slow", "scroller", "scroller_aft")
class ScrollerTest(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		test_files_path = os.path.join(os.path.dirname(__file__), 'testfiles', 'images')
		test_file_path = os.path.join(test_files_path, "list_test.png")
		global app
		app = App.open("mspaint " + test_file_path)
		wait(2)

	@classmethod
	def tearDownClass(cls):
		app.close()

	def setUp(self):
		self.scroller = Scroller()
		test_utils.skip_if_group_failed_or_skipped("unit")
	
	def tearDown(self):
		pass

	@raises(ValueError)
	def test_scroll_to_raises_ValueError(self):
		self.scroller.scroll_to()

	@raises(TimeoutException)
	def test_scroll_to_raises_TimeoutException(self):
		pattern = flex_label(text = "asdf")
		self.scroller.scroll_to(pattern_to_find = pattern, time_out = 3)

	def test_scroll_to_works(self):
		pattern = flex_label(text = "Pay Plans")
		self.scroller.scroll_to(pattern_to_find = pattern)

@attr("slow", "scroller", "scroller_aft")
class ScrollerNotFoundTest(unittest.TestCase):

	def setUp(self):
		if app is not None:
			app.close()
		self.scroller = Scroller()

	@raises(ScrollThumbNotFoundException)
	def test_scroll_to_raises_ScrollThumbNotFoundException(self):
		pattern = flex_label(text = "asdf")
		self.scroller.scroll_to(pattern_to_find = pattern, thumb_timeout = 0.2)