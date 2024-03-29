import traceback

Settings.MinSimilarity = .9
Settings.MoveMouseDelay = 0.75
setAutoWaitTimeout(120)

myPath = os.path.dirname(getBundlePath()) 
print "myPath = " + myPath
if not myPath in sys.path: sys.path.append(myPath)
print "sys.path = " +  str(sys.path)
try:
	from common.test_utils import TestRunner
	TestRunner().parse(sys.argv).execute()
	
except Exception as e:
	print "Error:", sys.exc_info()[1]
	print traceback.format_exc()
	raise e
