
from sikuli import *
from search import flex_image, flex_label, flex_button
from scroller import VScroller, HScroller
import alert
from config import Config
from utils import XmlUtils
from os import path
import project
from project import Project

common_icon = flex_image("Common.png",	background_color = "333333")
task_group_label = flex_label(text = "Task Group", font_color = "FFFFFF")
dropdown_menu = flex_image("DropDownMenu.png")


class TaskGroups:

	def __init__(self):
		self.project = Project()

	def ensure_screen_selected(self):
		click(common_icon)
		click(task_group_label)

	def add(self, group):
		self.ensure_screen_selected()
		self.project.edit()
		click(dropdown_menu)
		click(flex_label(text = "Add Template"))
		self._add(group)
		

	def _add(self, group):
		id_label = find(flex_label(text = "ID")).right(140).right(10)
		click(id_label)
		type("a", KeyModifier.CTRL) 
		paste(group.group_id)
		type(Key.TAB)
		wait(0.3)
		paste(group.name)
		type(Key.TAB)
		type("a", KeyModifier.CTRL) 
		paste(group.description)
		type(Key.TAB)
		type("S")
		task_group_resolver_drop_down = find(flex_label(text = "Task Group Resolver")).right(15).right(100)
		click(task_group_resolver_drop_down)
		resolver_area = task_group_resolver_drop_down.below(200)
		resolver_label = resolver_area.find(flex_label(text = group.task_group_resolver_name, font_weight = "bold"))
		click(resolver_label)
		escalate_to_drop_down = find(flex_label(text = "Escalate To")).right(55).right(100)
		click(escalate_to_drop_down)
		escalate_area = escalate_to_drop_down.below(200)
		escalate_to_label = escalate_area.find(flex_label(text = group.escalate_to, font_weight = "bold"))
		click(escalate_to_label)
		self.project.save()
		group.verify()

	def copy(self, group):
		self.ensure_screen_selected()
		self.project.edit()
		click(flex_label(text = group.copied_from, font_color = "FFFFFF"))
		click(dropdown_menu)
		click(flex_label(text = "Copy " + group.copied_from))
		self._add(group)

	def delete(self, group):
		self.ensure_screen_selected()
		self.project.edit()
		click(flex_label(text = group.name, font_color = "FF", font_weight = "bold"))
		click(dropdown_menu)
		click(flex_label(text = "Delete " + group.name))
		click(flex_button(text = "Yes", font_weight = "bold"))
		self.project.save()
		group.verify_deleted()


class TaskGroup:
	def __init__(self, copied_from = "Policy Review", group_id = None, name = None
			, description = None, task_group_resolver_name = None, deactivation_date = None
			, escalate_to = None, escalate_code = None, task_group_types_xml = None
			, config = None, file_path = None, task_group_rules_file_path = None):
		self.config = config or Config()
		self.copied_from = copied_from or "Policy Review"
		self.file_path = file_path or path.join(self.config.current_project_path, 'src/com/demo/uw/common/model/template/task-group.xml')
		self.task_group_rules_file_path = task_group_rules_file_path or path.join(self.config.current_project_path, 'powertools/task-group-rules.xml')
		self.load_from_copy(copied_from = copied_from)

		self.group_id = group_id or ""
		self.name = name or ""
		self.description = description or ""
		self.task_group_resolver_name = task_group_resolver_name
		self.deactivation_date = deactivation_date
		self.escalate_to = escalate_to
		self.escalate_code = escalate_code
		self.task_group_types_xml = task_group_types_xml or self.task_group_types_xml
		

	def load_from_copy(self, copied_from = "Policy Review"):
		copied_from = copied_from or self.copied_from or "Policy Review"
		xpath = "./TaskGroup[@Name='"+copied_from+"']"
		copied_xml = XmlUtils.getElement(self.file_path, xpath)
		if copied_xml is None:
			raise Exception("TaskGroup not found: with xpath {0} in file: {1}".format(xpath, self.file_path) )
		self.group_id = copied_xml.get("id")
		self.name = copied_xml.get("Name")
		self.description = copied_xml.get("Description")
		self.task_group_resolver_name = copied_xml.get("TaskGroupResolver")
		self.deactivation_date = copied_xml.get("DeactivationDt")
		self.escalate_to = copied_xml.get("EscalateTo")
		self.escalate_code = copied_xml.get("EscalateCode")
		self.task_group_types_xml = copied_xml[0]
	
	def to_xml(self):
		return_val = '<TaskGroup '
		if self.group_id is not None :
			return_val += 'id="'+self.group_id+'" '
		if self.name is not None :
			return_val += 'Name="'+self.name+'" '
		if self.description is not None :
			return_val += 'Description="'+self.description+'" '
		if self.task_group_resolver_name is not None and self.task_group_resolver_name != "Select...":
			resolver_class = self.get_task_group_resolver_class(self.task_group_resolver_name)
			return_val += 'TaskGroupResolver="' + resolver_class + '" '
		if self.deactivation_date is not None :
			return_val += 'DeactivationDt="'+self.deactivation_date+'" '
		if self.escalate_to is not None  and self.escalate_to != "Select...":
			return_val += 'EscalateTo="'+self.escalate_to+'" '
		if self.escalate_code is not None :
			return_val += 'EscalateCode="'+self.escalate_code+'" '
		return_val += '>'
		print self.task_group_types_xml
		if self.task_group_types_xml is not None:
			#yucky whitespace hack
			return_val += "\n    "
			return_val += XmlUtils.elementToString(self.task_group_types_xml)
		return_val += '</TaskGroup>'
		return return_val

	def get_task_group_resolver_class(self, rule_name):
		xpath = "./TaskGroupRule[@Name='" + rule_name + "']"
		result =  XmlUtils.getElementAttributeValue(
			  file_path = self.task_group_rules_file_path
			, element_xpath =  xpath
			, attribute = "TaskGroupResolver"
		)
		return result

	def verify(self):
		XmlUtils.assertElementsEqual (
			file_path = self.file_path
			, element_xpath = "./TaskGroup[@Name='"+self.name+"']"
			, expected_xml_string = self.to_xml()
		)

	def verify_deleted(self):
		element = XmlUtils.getElement(
			file_path = self.file_path
			, element_xpath = "./TaskGroup[@Name='"+self.name+"']"
		)
		assert element is None