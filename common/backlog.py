from sikuli import *
from search import flex_image, flex_label, flex_button
from scroller import VScroller

project_icon = flex_image("Project.png", 	background_color = "333333")
project_save = flex_image("ProjectSave.png",background_color = "333333")
project_edit = flex_image("ProjectEdit.png",background_color = "333333")
company_icon = flex_image("Company.png",	background_color = "333333")
backlog_plan_label = flex_label(text = "Backlog", font_color = "FFFFFF")
dropdown_menu = flex_image("DropDownMenu.png")

class Backlog:

	def __init__(self):
		self.vscroller = VScroller()

	def ensure_screen_selected(self):
		click(project_icon)
		click(backlog_plan_label)

	def close(self, item):
		if item is None:
			raise ValueError("item was not specified")
		self.ensure_screen_selected()
		click(flex_label(text = item.name))
		click(project_edit)
		wait(project_save)
		region = find(project_save).grow(5).below(150)
		region.click(dropdown_menu)
		click(flex_label(text = "Close"))
		click(project_save)
		wait(project_edit)
		self.refresh()

	def refresh(self):
		refresh_backlog_label = flex_label("Refresh Backlog")
		click(dropdown_menu)
		if(exists(refresh_backlog_label, 3) is not None):
			click(refresh_backlog_label)
			waitVanish(flex_label(
					text = "Refresh Backlog", font_color = "FFFFFF", font_size = 14, font_weight = "bold"
			))
			wait(2)

	def add(self, item):
		if item is None:
			raise ValueError("item was not specified")

		self.ensure_screen_selected()
		self.refresh()

		select_button = flex_button(
			text = "Select", font_weight = "bold", background_color = "D2E3F0"
		)

		click(project_edit)
		wait(project_save)

		click(dropdown_menu)
		click(flex_label(text = "Add Backlog Item"))

		#owner
		if item.owner == "signup":
			region = find(project_save).grow(5).below(150)
			region.click(dropdown_menu)
			click(flex_label("Sign Me Up"))

		#name
		region = find(flex_label(text = "Current Owner", font_color = "0"))
		region = region.above(5).above(20)
		region.click()
		type("a",KeyModifier.CTRL)
		type(Key.BACKSPACE)
		paste(item.name)

		#type
		region = find(flex_label("Type")).below(25)
		click(region)
		region = find(flex_label(
			text = item.type, font_weight = "bold"
		))
		click(region)

		#estimate
		region = find(flex_label("Estimate")).below(25)
		click(region)
		paste(item.estimate)

		#description
		region = find(flex_label("Description")).below(25)
		click(region)
		paste(item.description)

		#configurable areas
		print 'len(item.configurable_areas) = ' + str(len(item.configurable_areas))
		if len(item.configurable_areas) > 0:
			region = find(flex_label(
				text = "Configurable Areas", font_weight = "bold"
			)).grow(5).right()
			region.click(dropdown_menu)

			click(flex_label("Assign Configurable Areas"))
			#the list we're scrolling is alphabetical
			#so sort the config areas list
			for area in sorted(item.configurable_areas):
				print area
				image_name = flex_label(area)
				self.vscroller.scroll_to(image_name)
				click(image_name, KeyModifier.CTRL)

			click(select_button)

		click(project_save)
		wait(project_edit, 120)

class BacklogItem:

	def __init__(self, name = "", owner = "signup", item_type = "Basic Configuration", 
		estimate = "0", description = "", configurable_areas = None):
		self.name = name
		self.owner = owner
		self.type = item_type
		self.estimate = estimate
		self.description = description
		self.configurable_areas = configurable_areas or []


