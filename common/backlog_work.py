from sikuli import *
from search import flex_image, flex_label, flex_button
import alert

project_icon = flex_image("Project.png", background_color = "0")
backlog_work_icon = flex_image("BacklogWork.png", background_color="577694")
dropdown_menu = flex_image("DropDownMenu.png")
working_icon = flex_image("Working22.png")
released_icon = flex_image("Approved.png")

my_work_label = flex_label(text = "My Work", font_size = 14, font_weight = "bold")
reserved_areas_label = flex_label(text = "Reserved Areas", font_size = 14)
completed_label = flex_label(text = "Completed", font_size = 14)
released_label = flex_label(text = "Released", font_size = 14)

class BacklogWork:

	def ensure_screen_selected(self):
		click(project_icon)
		click(backlog_work_icon)

	def release_configurable_area(self, configurable_area):
		self.ensure_screen_selected()
		work_label_region = find(my_work_label).grow(10).left()
		region = work_label_region.find(dropdown_menu)
		click(region)
		click(flex_label("Refresh My Work"))
		wait(1)
		work_region = Region(region.x - 5, region.y + 20, 370, 70)
		config_area_label = work_region.find(flex_label(text = configurable_area))
		working_icon_region = config_area_label.grow(50).right().find(working_icon)
		completed_region = find(completed_label).below(5).grow(150, 0).below(100)
		released_region = find(released_label).below(5).grow(150, 0).below(100)
		dragDrop(working_icon_region, completed_region)
		click(alert.yes_button)
		released_region.wait(released_icon, 30)

	def undo_work_item(self, item):
		pass