import os
from aft_model import AftModel
try:
	import xml.etree.cElementTree as ET
except:
	import xml.etree.ElementTree as ET


class AppDescriptor(object):

	def __init__(self, file_path = None):
		self.aft_model = AftModel()
		self.file_path = file_path or os.path.join(self.aft_model.project_root(), "src\PowerToolsDesktop-app.xml")
		self.namespace = "{http://ns.adobe.com/air/application/3.1}"
	
	def version_number(self):
		version_number = "0.0.0"
		tree = ET.parse(self.file_path)
		element = tree.find("{0}versionNumber".format(self.namespace))
		version_number = element.text
		return version_number

	def version_label(self):
		version_label = "0.0.0"
		tree = ET.parse(self.file_path)
		element = tree.find("{0}versionLabel".format(self.namespace))
		version_label = element.text
		return version_label

	def app_id(self):
		app_id = "com.nothing"
		tree = ET.parse(self.file_path)
		element = tree.find("{0}id".format(self.namespace))
		app_id = element.text
		return app_id