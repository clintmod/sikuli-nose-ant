
from sikuli import *
from search import flex_image, flex_label, flex_button
from scroller import VScroller, HScroller
import alert
from config import Config
from utils import XmlUtils
from os import path
import project
from project import Project
from images import checked_checkbox
from nose.tools import assert_equal

common_icon = flex_image("Common.png",	background_color = "333333")
note_template_image = flex_image("CommonNotes.png", background_color="577694", height = 32, width = 32)
dropdown_menu = flex_image("DropDownMenu.png")

class NoteTemplates:

	def __init__(self):
		self.project = Project()

	def ensure_screen_selected(self):
		click(common_icon)
		click(note_template_image)

	def click_dropdown_menu(self):
		region = find(flex_label(text = "Underwriting Note Templates", font_color = "FFFFFF", font_size = 14, font_weight = "bold")).grow(5).right()
		click(region.find(dropdown_menu))

	def add(self, template):
		self.ensure_screen_selected()
		self.project.edit()
		copy_from =  template.copy_from['name'] + "   " + "(" + template.copy_from['package'] + ")"
		click(flex_label(text = copy_from, font_color = "FFFFFF"))
		self.click_dropdown_menu()
		click(flex_label(text = "Copy " + template.copy_from['name']))
		click(flex_button(text = "General", font_color = "8C8C8C", font_weight = "bold"))
		
		if "Quick Quote" in template.available_on:
			click(flex_label(text="Quick Quote"))

		for label in template.available_on:
			print label
			if label != "Quick Quote":
				self.check_checkbox_if_unchecked(label)
		id_field = find(flex_label(text = "ID")).right(100).right(100)
		click(id_field)
		#type("a", KeyModifier.CTRL)
		#paste(template.template_id)
		type(Key.TAB)
		wait(0.2)
		paste(template.name)
		type(Key.TAB)
		wait(0.2)
		type(Key.TAB)
		wait(0.2)
		type(Key.TAB)
		wait(0.2)
		type(Key.TAB)
		wait(0.2)
		type("a", KeyModifier.CTRL)
		paste(template.description)
		self.project.save()
		template.verify()

	def check_checkbox_if_unchecked(self, label):
		label_region = find(flex_label(text = label))
		region = label_region.grow(2).left(30)
		if region.exists(checked_checkbox, 1) is None:
			click(label_region)

	def delete(self, template):
		self.ensure_screen_selected()
		self.project.edit()
		added_label = flex_label(text = template.name, font_color = "0000FF", font_weight="bold")
		existing_label = flex_label(text = template.name, font_color = "FFFFFF")
		if exists(added_label, 0.5):
			click(added_label)
		elif exists(added_label, 0.5):
			click(existing_label)
		self.click_dropdown_menu()
		click(flex_label(text = "Delete " + template.name))
		click(flex_button(text = "Yes", font_weight = "bold"))
		self.project.save()
		template.verify_deleted()

class NoteTemplate:

	def __init__(self, name = None, copy_from = None, description = None
			, available_on = ["Quote"], config = None, file_map = None):
		self.config = config or Config()
		self.copy_from = copy_from
		self.name = name
		self.description = description
		self.available_on = available_on or ["Quote"]
		self.file_map = file_map or {
			"Quote":path.join(self.config.current_project_path, 'src/com/demo/uw/quote/model/template/note.xml')
			, "Application":path.join(self.config.current_project_path, 'src/com/demo/uw/app/model/template/note.xml')
			, "Policy":path.join(self.config.current_project_path, 'src/com/demo/uw/policy/model/template/note.xml')
		}

	def verify(self):
		xpath = "./NoteTemplate[@Name='"+self.name+"']"
		for package in self.available_on:
			file_path = self.file_map[package]
			print file_path
			element = XmlUtils.getElement(file_path = file_path, element_xpath = xpath)
			assert element is not None, "element was None xpath: {0} file: {1}".format(xpath, file_path)
			assert_equal(element.get("Description"), self.description)
		

	def verify_deleted(self):
		xpath = "./NoteTemplate[@Name='"+self.name+"']"
		for package in self.available_on:
			file_path = self.file_map[package]
			print file_path
			element = XmlUtils.getElement(
				file_path = file_path
				, element_xpath = xpath
			)
			assert element is None, "element was found with xpath: {0} file: {1}".format(xpath, file_path)
