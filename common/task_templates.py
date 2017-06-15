
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

task_template_image = flex_image("CommonTasks.png", background_color="577694")
common_icon = flex_image("Common.png",	background_color = "333333")
dropdown_menu = flex_image("DropDownMenu.png")

class TaskTemplates:

	def __init__(self):
		self.project = Project()

	def ensure_screen_selected(self):
			click(common_icon)
			click(task_template_image)

	def add(self, template):
		self.ensure_screen_selected()
		self.project.edit()
		click(dropdown_menu)
		click(flex_label(text = "Add Template"))
		click(flex_button(text = "General", font_color = "8C8C8C", font_weight = "bold"))
		package_label = find(flex_label(text="Quick Quote"))
		if template.package != "Quick Quote":
			package_label = package_label.grow(5).right().find(flex_label(text = template.package))
		click(package_label)
		click(flex_label(text = template.package))
		type(Key.TAB)
		wait(0.2)
		paste(template.template_id)
		type(Key.TAB)
		wait(0.2)
		paste(template.name)
		type(Key.TAB)
		wait(0.2)
		type(template.task_type[0]) #first character (e.g. M in Manual)
		type(Key.TAB)
		wait(0.2)
		type(Key.TAB)
		wait(0.2)
		type(Key.TAB)
		wait(0.2)
		paste(template.text)
		type(Key.TAB)
		wait(0.2)
		paste(template.description)
		self.check_checkbox_if_unchecked(label = "Work Required")
		self.check_checkbox_if_unchecked(label = "Show on Inbox")
		assignment_label = flex_button(text = "Assignment", font_color = "777777", font_weight = "bold")
		click(assignment_label)
		owner_type_drop_down = find(flex_label(text = "Owner Type")).right(15).right(150)
		click(owner_type_drop_down)
		owner_type_drop_down.below(300).click(flex_button(text = template.assignment_owner_type, font_weight = "bold"))
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
		click(dropdown_menu)
		click(flex_label(text = "Delete " + template.name))
		click(flex_button(text = "Yes", font_weight = "bold"))
		self.project.save()
		template.verify_deleted()

class TaskTemplate:

	def __init__(self, template_id = None, name = None, task_type = None, text = None
			, description = None, work_required = False, show_in_inbox = False
			, assignment_owner_type = None, package = "Quick Quote", file_path = None
			, config = None):
		self.config = config or Config()
		self.file_path = file_path or path.join(self.config.current_project_path
			, 'src/com/demo/uw/quote/model/template/task.xml')
		self.template_id = template_id or ""
		self.name = name or ""
		self.task_type = task_type or ""
		self.text = text or ""
		self.description = description or ""
		self.work_required = work_required or False
		self.show_in_inbox = show_in_inbox or False
		self.assignment_owner_type = assignment_owner_type
		self.package = package or "Quick Quote"

	def verify(self):
		xpath = "./TaskTemplate[@Name='"+self.name+"']"
		element = XmlUtils.getElement(file_path = self.file_path, element_xpath = xpath)
		assert element is not None, "element was None xpath: {0} file: {1}".format(xpath, self.file_path)
		assert_equal(element.get("id"),  self.template_id)
		assert_equal(element.get("Text"), self.text)
		assert_equal(element.get("Description"), self.description)
		assert_equal(element.get("DefaultOwnerCd"), self.assignment_owner_type)
		assert_equal(element.get("TaskTypeCd"), self.task_type)
		assert_equal(element.get("ShowOnInboxInd"), self.convert_bool_to_yes_no(self.show_in_inbox))
		assert_equal(element.get("WorkRequiredInd"), self.convert_bool_to_yes_no(self.work_required))

	def verify_deleted(self):
		xpath = "./TaskTemplate[@Name='"+self.name+"']"
		element = XmlUtils.getElement(
			file_path = self.file_path
			, element_xpath = xpath
		)
		assert element is None, "element was found with xpath: {0} file: {1}".format(xpath, self.file_path)

	def convert_bool_to_yes_no(self, val):
		if val == True :
			return "Yes"
		else :
			return "No"