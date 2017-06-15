from sikuli import *
from template import ProjectTemplate
from utils import ScreenUtils
from search import flex_image, flex_label, flex_button
from images import system_folder_label

project_save = flex_image("ProjectSave.png",background_color = "333333")
project_edit = flex_image("ProjectEdit.png",background_color = "333333")
powertools_icon = flex_image("icon_024.png", height = 24, width = 24)
close_icon = flex_image("CloseButton.png", height = 16, width = 16)
common_icon = flex_image("Common.png", background_color = "0")
server_stopped_icon = flex_image("ServerStopped.png", background_color = "0")
create_or_join_label = flex_label(text = "Create or join a project", font_color = "FFFFFF", font_size = 14)
#the below button matches Create Project and Join Project
project_partial_button = flex_button(text = "Project", font_color = "FFFFFF", font_size = 11, font_weight = "bold", background_color = "3A546D")
project_label = flex_label(text = "Innovative Insurance Company", font_color = "FFFFFF", font_size = 14)
yes_button = flex_button(text = "Yes", font_weight="bold")
project_icon_black = flex_image("Project.png", 	background_color = "333333")
project_icon_blue = flex_image("Project.png", background_color = "577694")
dropdown_menu = flex_image("DropDownMenu.png")

class Project(object):
 
	def __init__(self, template = None):
		self.project_template = template or ProjectTemplate()
		self.screen_utils = ScreenUtils()
		self.path = ""

	def close_dialog(self):
		region = find(powertools_icon)
		region = region.below().right()
		if region.exists(close_icon, 3):
			region.click(close_icon)
	
	def create_or_join(self, path = None):
		if(exists(common_icon, 3) is not None):
			return
		if(path is None):
			path = self.project_template.clone_if_current_project_not_set()
		self.path = path 
		if exists(create_or_join_label,1) is None:
			self.click_open_or_create_menu_item()
		click(create_or_join_label)
		click(flex_image("SelectFolderButton.png", background_color = "92B6DC", height = 20, width = 23))
		wait(system_folder_label)
		region = find(system_folder_label).right(10)
		click(region)
		paste(self.path)
		type(Key.TAB)
		type(Key.ENTER)
		wait(project_partial_button, 60 * 3) #3 minutes
		click(project_partial_button)
		
		self.wait_for_main_screen(60 * 20) #20 minutes
		stopObserver()
		return self.path

	def open_powertools_menu(self):
		click(powertools_icon)
	
	def click_open_or_create_menu_item(self):
		self.open_powertools_menu()
		click(flex_label(text = "Open/Create Project"))

	def open(self):
		self.click_open_or_create_menu_item()
		self._open()
	
	def _open(self):
		click(project_label)
		self.wait_for_main_screen(60 * 2)
	
	def open_or_create_or_join(self, path = None, should_remove_if_open = False):
		if(exists(common_icon, 3) is not None):
			return "project already open"
		self.click_open_or_create_menu_item()
		if(exists(project_label, 3) is not None):
			if should_remove_if_open:
				self.remove_local()
				return self.create_or_join(path)
			else:
				self._open()
				return "opened"
		else:
			return self.create_or_join(path)
	
	def wait_for_main_screen(self, timeout):
		def dismiss_update_workspace(event):
			click(yes_button)
			stopObserver()
		onAppear(yes_button, dismiss_update_workspace)
		observe(FOREVER, True)
		wait(server_stopped_icon, timeout)
		stopObserver()
		
	def delete_locally_and_from_server(self):
		click(project_icon_black)
		click(project_icon_blue)
		click(flex_button(text = "Advanced", font_color = "8C8C8C", font_weight = "bold"))
		click(flex_label(text = "Delete from Server"))
		click(flex_button(text = "Delete Project", font_weight = "bold"))
		region = find(flex_image("Hoop.png")).below(10).below(20)
		region.highlight(1)
		click(region)
		paste("innovation1")
		click(flex_button(text = "Delete Permanently!", font_weight = "bold"))
		click(flex_button(text = "Yes", font_weight = "bold"))
		wait(1)
		waitVanish(project_icon_black, 60 * 5) #5 minutes

	def close(self):
		self.open_powertools_menu()
		click(flex_label(text = "Close Project"))
		wait(1)
		assert exists(common_icon, 3) is None

	def restart(self):
		self.close()
		self.open()

	def edit(self):
		if exists(project_save, 0.3) is None:
			click(project_edit)
			wait(project_save)

	def save(self):
		click(project_save)
		wait(project_edit)
