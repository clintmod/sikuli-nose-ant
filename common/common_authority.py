from sikuli import *
from search import flex_image, flex_label, flex_button
from scroller import VScroller, HScroller
import alert
from config import Config
from utils import XmlUtils
from os import path
import project
from project import Project

common_icon = flex_image("Common.png",	background_color = "0")
authority_image = flex_image("CommonAuthority.png", background_color="577694")
dropdown_menu = flex_image("DropDownMenu.png")

class CommonAuthority:

	def __init__(self):
		self.project = Project()

	def ensure_screen_selected(self):
		click(common_icon)
		click(authority_image)

	def delete_attribute(self, attribute):
		if attribute is None:
			raise ValueError("attribute was not specified")

		self.ensure_screen_selected()
		click(flex_label(text = attribute.authority_set, font_color = "FFFFFF"))
		self.project.edit()
		click(flex_label(attribute.name))
		region = find(project.project_save).grow(5).below(150)
		region.click(dropdown_menu)
		click(flex_label("Edit " + attribute.name))
		click(flex_button(text = "Delete", font_weight = "bold"))
		click(alert.yes_button)
		self.project.save()

	def add_attribute(self, attribute):
		if attribute is None:
			raise ValueError("attribute was not specified")

		self.ensure_screen_selected()

		click(flex_label(text = attribute.authority_set, font_color = "FFFFFF"))
		self.project.edit()
		region = find(project.project_save).grow(5).below(150)
		region.click(dropdown_menu)
		click(flex_label(text = "Add Attribute"))
		region = find(flex_button(text = "Unique ID", background_color = "92B7DB")).right(40).right(40)
		
		click(region)
		paste(attribute.id)
		type(Key.TAB)
		paste(attribute.name)
		type(Key.TAB)
		paste(attribute.description)
		type(Key.TAB)
		paste(attribute.default_value)
		region = find(flex_label(text = "Data Type")).right(40).right(40)
		
		click(region)
		click(flex_label(text = attribute.data_type, font_weight = "bold"))
		click(flex_button(text = "Save", font_weight = "bold"))
		self.project.save()
		attribute.verify_authority_set()

	def set_role_permissions(self, attribute):
		vscroller = VScroller()
		hscroller = HScroller()
		name_label = flex_label(attribute.name)
		name_region = vscroller.scroll_to(name_label)
		print "name_region = " + str(name_region)
		self.project.edit()
		for role, value in sorted(attribute.role_permissions):
			#horizontally scroll until we find the role
			role_label = flex_label(text = role)
			role_region = hscroller.scroll_to(role_label)
			print "role_region = " + str(role_region)
			intersection = Location(role_region.x + 5, name_region.y + 5)
			click(intersection)
			wait(1)
			paste(value)
		self.project.save()

	def copy_role(self, name, role):
		self.project.edit()
		role_label = flex_label(text = name)
		hscroller = HScroller()
		hscroller.scroll_to(role_label)
		click(role_label)
		click(flex_button(text = "Copy", font_weight = "bold"))
		unique_id_label = flex_button(text = "Unique ID", background_color = "92B7DB")
		unique_id_text_field = find(unique_id_label).right(10).right(30)
		click(unique_id_text_field)
		type("a", KeyModifier.CTRL) 
		paste(role.uid)
		type(Key.TAB)
		paste(role.name)
		type(Key.TAB)
		paste(role.description)
		type(Key.TAB)
		paste(role.area)
		click(flex_button(text = "Save", font_weight = "bold"))
		self.project.save()
		


class AuthorityAttribute:

	def __init__(self, authority_set, attribute_id, name, description, default_value
			, data_type, role_permissions = None, config = None, file_path = None):
		self.config = config or Config()
		self.file_path = file_path or path.join(self.config.current_project_path, 'src/com/demo/common/shared/model/template/authority-set.xml')
		self.authority_set = authority_set
		self.id = attribute_id
		self.name = name
		self.description = description
		self.default_value = default_value
		self.data_type = data_type
		self.role_permissions = role_permissions or []

	def to_xml(self):
		return_val = '<AuthorityAttribute id="'+self.id+'" '
		return_val += 'Name="'+self.name+'" '
		return_val += 'Description="'+self.description+'" '
		return_val += 'DataTypeCd="'+self.data_type+'" '
		return_val += 'DefaultValue="'+self.default_value+'" />'
		return return_val

	def verify_authority_set(self):
		XmlUtils.assertElementsEqual (
			  file_path = self.file_path
			, element_xpath = "./AuthorityAttributeSet[@Name='"+self.authority_set+"']/AuthorityAttribute[@id='" + self.id + "']"
			, expected_xml_string = self.to_xml()
		)

class AuthorityRole:
	
	def __init__(self, uid, name, description, area):
		self.uid = uid
		self.name = name
		self.description = description
		self.area = area