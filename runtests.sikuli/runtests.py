import traceback

Settings.MinSimilarity = .9
Settings.MoveMouseDelay = 0.75
setAutoWaitTimeout(120)

try:
	from common.test_utils import TestRunner
	TestRunner().parse(sys.argv).execute()
	
except Exception as e:
	print "Error:", sys.exc_info()[1]
	print traceback.format_exc()
	raise e
