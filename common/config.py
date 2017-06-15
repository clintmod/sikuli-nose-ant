import os
import json
from aft_model import AftModel

class Config(object):

	def __init__(self, config_file_path = None):
		self.aft_model = AftModel()
		self.config_file_path = config_file_path or os.path.join(
			self.aft_model.project_root(), "..", "powertools_aft_config.json"
		)
		self.json_object = JsonObject()
		self.load_config()

	@property
	def current_project_path(self):
		path = self.get_property_value("current_project_path")
		return path

	@current_project_path.setter
	def current_project_path(self, path):
		if path and not os.path.exists(path):
			raise ValueError("path does not exist")
		self.set_property_value("current_project_path", path)
		

	def set_property_value(self, prop_name, prop_value):
		setattr(self.json_object, prop_name, prop_value)
		self.save_config()

	def get_property_value(self, prop_name):
		if hasattr(self.json_object, prop_name):
			return self.json_object.__dict__[prop_name]
		else:
			return None

	def save_config(self):
		json_string = self.json_object.to_json();
		with open(self.config_file_path, 'w+') as file_handle:
   			file_handle.write(json_string)
   		assert os.path.exists(self.config_file_path)

	def load_config(self):
		if not os.path.exists(self.config_file_path) : return
		with open(self.config_file_path, "r+") as file_handle:
   			json_string = file_handle.read()
		self.json_object.from_json(json_string)
		file_handle.close()

	def flush_config(self):
		self.json_object = JsonObject()

	def delete_config(self):
		self.flush_config()
		if os.path.exists(self.config_file_path):
			os.remove(self.config_file_path)


class JsonObject(object):

	def to_json(self):
		return json.dumps(self.__dict__)

	def from_json(self, json_string):
		self.__dict__ = json.loads(json_string)