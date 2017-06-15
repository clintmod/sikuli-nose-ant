from sikuli import *
import traceback

try:
	from common import *
	from common.template import ProjectTemplate
	from common.utils import ScreenUtils
	from common.installer import *

	project_template = ProjectTemplate()
	project = Project(template = project_template)
	workspace = Workspace()
	screen_utils = ScreenUtils()
	installer = Installer()
	powertools = PowerTools()

	installerx_model = InstallerModel(app_name = "PowerTools Desktop X")
	installerx = Installer(model = installerx_model)
	powertoolsx = PowerTools(model = installerx_model)

	# print sys.argv
	# exec(sys.argv[1])

	exec(sys.argv[1])
except (Exception, FindFailed) as e:
	screen_utils = ScreenUtils()
	file_path = screen_utils.capture_screen()
	print "Error:", sys.exc_info()[1]
	print traceback.format_exc()
	print "Captured screen shot at: " + file_path
	print "---------------------------\n"
	wait(1)
	raise e