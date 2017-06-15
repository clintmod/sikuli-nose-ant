import os; from os import path
from sikuli import *
import traceback
from common import PowerTools, Workspace, Project
from common.template import ProjectTemplate
from common.utils import ScreenUtils
from common.scroller import VScroller

Settings.OcrTextSearch = True
Settings.OcrTextRead = True
#this needs to be .9 or the edit icon will match the cancel icon (pencil vs. x)
Settings.MinSimilarity = .9
setAutoWaitTimeout(120)
FIVE_MINUTES = 60 * 5

try:
	powertools = PowerTools()
	region = powertools.open()
	
	def app_error(event):
		raise Exception("An error occured.")
	region.onAppear("1424300912166.png", app_error)
	
	workspace = Workspace()
	workspace.configure_if_required("johnny1", "asdf1234")
	
	project_template = ProjectTemplate()
	project = Project(project_template)
	path = project.open_or_create_or_join()

	#project_template.clone_name = "749bf8cd-8b7a-4197-a8d6-68d025f60034"
	#path = "created"

	cloned_path = project_template.full_clone_path()

	if(path != "opened"):
		print "checking out project for devx"
		project_template.checkout_project_from_cvs("ptcvsuser2", "_copy")

	wait("1417485496099.png")
	click("1417485496099.png")
	wait("1417484062075.png")
	wait("1417481345687.png")
	click("1417481345687.png")
	click("1417550609672.png")
	region = find("1417550637810.png").below(20)
	click(region)
	type("a",KeyModifier.CTRL)
	type(Key.BACKSPACE)

	paste("Update Company Name")
	find("1417484062075.png").below(150).click("1417481345687.png")
	click("1417556044158.png")
	click("1417556097855.png")
	type("B")
	type(Key.TAB)
	type("1")
	find("1417481292451.png").right().click("1417481345687.png")
	click("1423509606590.png")
	vscroller = VScroller("1417482847118.png")
	vscroller.scroll_to("1425674113349.png")
	doubleClick("1425674113349.png")
	click("1417484062075.png")
	wait("1417485496099.png")
	click("1417484201724.png")
	click("1425680330421.png")
	click("1417485496099.png")
	wait("1417484062075.png")
	region = find("1425680349421.png").right(30)
	doubleClick(region)
	paste("Suite 210")
	click("1417484062075.png")
	wait("1417485496099.png")
	click("1418330539729.png")
	click("1425681710630.png")
	region = find("1425681791762.png").below()
	reserved = find("1425681791762.png").below()
	completed = find("1425682020021.png").below(100)
	work_item = reserved.find("1425681929601.png")
	dragDrop(work_item, completed)
	click("1417557484758.png")
	wait(Pattern("1425682263806.png").exact())
	powertools.close()

	powertoolsX = PowerTools("PowerTools Desktop X")
	powertoolsX.open()

	workspace.configure_if_required()

	projectX = Project()
	projectX.open_or_create_or_join(cloned_path + "_copy")

	wait("1417485496099.png")
	click("1417484201724.png")
	click("1425680330421.png")
	region = find("1425680349421.png").right()
	region.find("Suite 210")
	print "Success: Suite 210 found."
	
except (Exception, FindFailed) as e:
	screen_utils = ScreenUtils()
	file_path = screen_utils.capture_screen()
	print "Error:", sys.exc_info()[1]
	print traceback.format_exc()
	print "Captured screen shot at: " + file_path
	print "---------------------------\n"
	wait(1)
	raise e
