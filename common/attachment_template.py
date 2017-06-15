from sikuli import *
from search import flex_image, flex_label, flex_button
from scroller import VScroller, HScroller, Scroller
import alert
from config import Config
from utils import XmlUtils
from os import path
import project
from project import Project
from images import checked_checkbox
from nose.tools import assert_equal
from images import drop_down_arrow

common_icon = flex_image("Common.png",	background_color = "0")
attachment_template_image = flex_image("CommonAttachments.png", background_color="577694")
dropdown_menu = flex_image("DropDownMenu.png")


class AttachmentTemplates: #attachment_template

	def __init__(self):
		self.project = Project()
		self.scroller = Scroller()

	def ensure_screen_selected(self):
		click(common_icon)
		click(attachment_template_image)


	def click_dropdown_menu(self):
		region = find(flex_label(text = "Underwriting Attachment Templates", font_color = "FFFFFF", font_size = 14, font_weight = "bold", background_color = "7F9CBA")).grow(5).right()
		click(region.find(dropdown_menu))	
	

	def add(self, template):

		self.ensure_screen_selected()
		self.project.edit()
		self.click_dropdown_menu()
		click(flex_label(text = "Add Template" ))		
		click(flex_button(text = "General", font_color = "8C8C8C", font_weight = "bold"))
		
		
 		if "Quick Quote" in template.available_on:
			click(flex_label(text="Quick Quote"))

		for label in template.available_on:
			print label
			if label != "Quick Quote":
				self.check_checkbox_if_unchecked(label)
		id_field = find(flex_label(text = "ID")).right(100).right(100)
		click(id_field)
		type("a", KeyModifier.CTRL)
		paste(template.template_id)
		type(Key.TAB)
		wait(0.2)
		paste(template.name)
		type(Key.TAB)
		wait(0.2)
		type(Key.TAB)
		wait(0.2)
		type("a", KeyModifier.CTRL)
		paste(template.description)
		type(Key.TAB)
		wait(0.2)
		paste(template.comments)

		

		click(flex_button(text = "Tags", font_color = "8C8C8C", font_weight = "bold"))		
		region = find(flex_label(text = "Tag Templates", font_color = "0", font_size = 14, font_weight = "bold", background_color = "7F9CBA")).grow(5).right()
		click(region.find(dropdown_menu))		
		click(flex_label(text = "Add" ))
		self.add_dropdown_value_Tags("Application","Default")	



		click(flex_button(text = "Security", font_color = "8C8C8C", font_weight = "bold"))	
		self.set_dropdown_value("Add", "Yes")
		self.set_dropdown_value("Edit", "Yes")	
		self.set_dropdown_value("EditAttachment", "No")		
		self.set_dropdown_value("View", "Yes")				
		self.set_dropdown_value("Delete", "No")		
		self.set_dropdown_value("Copy", "Yes")		
		self.set_dropdown_value("Move", "No")		
		self.set_dropdown_value("Annotate", "Yes")

		self.project.save()
		template.verify()



	def set_dropdown_value(self, label_text, value):
		region = find(flex_label(text = label_text, font_color = "0", font_size = 11, font_weight = "normal", background_color = "FFFFFF"))
		click(region.right(80).right(20))
		wait(.5)
		drop_down_region = region.grow(20).right().find(drop_down_arrow).grow(5).left().below(120)
		#drop_down_region.highlight(1)
		drop_down_region.click(flex_label(text = value, font_color = "0", font_size = 11, font_weight = "bold", text_align = "left" ))




	def add_dropdown_value_Tags(self, label_text, value):	
		click(flex_label(text = "Attachment Method", font_color = "0", font_size = 12, font_weight = "normal",background_color ="B2E1FF"))
		region = flex_label(text = "Optional", font_color = "0", font_size = 12, font_weight = "normal",background_color ="B2E1FF")
		click(region)
		wait(0.5)
		click(flex_label(text = "Optional", font_color = "0", font_size = 12, font_weight = "bold",background_color ="C8E3F4"))
		click(flex_label(text = value, font_color = "0", font_size = 12, font_weight = "bold",background_color ="FFFFFF"))
		wait(0.5)


		
		region = find(flex_label(text = "Name", font_color = "0", font_size = 12, font_weight = "normal", background_color = "B2E1FF"))
		click(region.right(80).below(60))
		wait(.5)
		self.scroll_to_and_click(label_text)

		

	def scroll_to_and_click(self, label_text):
			region=find(flex_label(text = "Select Tag...", font_color = "0", font_size = 12, font_weight = "bold",background_color ="C8E3F4"))
			click(region)	

			regioninput = Region(region.x - 15, region.y, region.w + 700, region.h + 700)
			#regioninput.highlight(2)
			pattern = flex_label(text = "Quote", font_color = "0", font_size = 12, font_weight = "bold", text_align = "left")
			self.scroller.scroll_to(pattern_to_find = pattern, region = regioninput, time_out = 10)			
			click(pattern, KeyModifier.CTRL)
			#click(flex_label(text = label_text, font_color = "0", font_size = 12, font_weight = "bold",background_color ="FFFFFF"))

	

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
		wait(.2)
		click(flex_button(text = "Yes", font_weight = "bold"))
		wait(.2)
		self.project.save()
		template.verify_deleted()



class AttachmentTemplate(): #template

	def __init__(self, template_id, name = None, description = None
			, comments = None, available_on = ["Quote"], config = None
			, file_map = None):
		self.config = config or Config() 
		self.template_id = template_id
		self.name = name
		self.description = description
		self.comments =  comments
		self.available_on = available_on or ["Quote"]
		self.file_map = file_map or {
			"Quote":path.join(self.config.current_project_path, 'src/com/demo/uw/quote/model/template/attachment.xml')
			, "Application":path.join(self.config.current_project_path, 'src/com/demo/uw/app/model/template/attachment.xml')
			, "Policy":path.join(self.config.current_project_path, 'src/com/demo/uw/policy/model/template/attachment.xml')
			
		}

	def verify(self):

		xpath = "./AttachmentTemplate[@Name='"+self.name+"']"
		for package in self.available_on:
			file_path = self.file_map[package]
			print file_path
			element = XmlUtils.getElement(file_path = file_path, element_xpath = xpath)
			assert element is not None, "element was None xpath: {0} file: {1}".format(xpath, file_path)
			assert_equal(element.get("Description"), self.description)
			print "verifyyy Passed"
		

	def verify_deleted(self):
		xpath = "./AttachmentTemplate[@Name='"+self.name+"']"
		for package in self.available_on:
			file_path = self.file_map[package]
			print file_path
			element = XmlUtils.getElement(
				file_path = file_path
				, element_xpath = xpath
			)
			assert element is None, "element was found with xpath: {0} file: {1}".format(xpath, file_path)
			print "verifyyy_delete Passed"
