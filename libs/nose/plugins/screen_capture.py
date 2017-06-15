import traceback
import nose
from nose.plugins import Plugin
from nose.pyversion import exc_to_unicode, force_unicode

from common.utils import ScreenUtils

screen_utils = ScreenUtils()

class ScreenCapture(Plugin):

	name = 'screen-capture'
	enabled = True


 	def formatError(self, test, err):
		return self.add_screen_capture_path(test, err)
			
	def formatFailure(self, test, err):
		return self.add_screen_capture_path(test, err)

	def add_screen_capture_path(self, test, err):
		location = screen_utils.capture_screen(verbose=False)
		ec, ev, tb = err
		ev = exc_to_unicode(ev)
		output = force_unicode(location)
		ev = ev + u"\ncaptured screen shot at:" + location
		return (ec, ev, tb)
		