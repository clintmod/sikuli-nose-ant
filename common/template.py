import os
import re
import uuid
from os import sep, path
from shutil import copytree
from utils import Shell, XmlUtils
from environment_model import EnvironmentModel
from config import Config
nix_sep = "/"

class ProjectTemplate(object):

	def __init__(self, config = None):
		self.shell = Shell(verbose = True)
		self.environment_model = EnvironmentModel()
		self.config = config or Config()
		self.clones_folder = "custDEMO-clone"
		self.clone_name = str(uuid.uuid4())
		self.cvs_user = "ptcvsuser1"
		self.cvs_server = "sj1-qa02.somecompany.net"	
		self.cvs_repo = "/home/cvs/ptsandbox"
		if self.config.current_project_path is not None and path.exists(self.config.current_project_path):
			self.load_cvs_settings_from_current_project_path()

	def clone(self):
		self.clone_name = str(uuid.uuid4())
		self.delete_compiled_java_files()
		self.update_power_tools_xml()
		self.create_project_from_template()

		return self.full_clone_path()

	def clone_if_current_project_not_set(self):
		if(self.config.current_project_path is None):
			self.clone()
		return self.full_clone_path()

	def delete_compiled_java_files(self):
		path = self.template_dir()
		exts = ['.class']
		for root, dirs, files in os.walk(path):
			for fle in files:
				if any(fle.lower().endswith(ext) for ext in exts):
					os.remove(os.path.join(root, fle))

	def create_project_from_template(self):
		print "cloning project"
		self.import_template_to_cvs_as_new_project()
		self.checkout_project_from_cvs()
		self.config.current_project_path = self.full_clone_path()
		assert self.config.current_project_path is not None
		self.update_eclipse_project_file()
		self.ensure_all_dirs_from_src_exist_in_dest(self.template_dir(), self.full_clone_path())
		print "cloned project to: " + self.full_clone_path()

	def ensure_all_dirs_from_src_exist_in_dest(self, src, dest):
		for root, dirs, files in os.walk(src):
			if "CVS" in dirs: dirs.remove("CVS")
			for dir_name in dirs:
				full_dir = str(root) + "\\" + dir_name
				sub_path = path.relpath(full_dir, src)
				new_path = path.join(dest,sub_path)
				if not path.exists(new_path):
					os.mkdir(new_path)
					pass

	def import_template_to_cvs_as_new_project(self):
		self.shell.execute("cvs -d " + self.cvs_url() + " import -m \"Initial Import\" " 
			+ self.cvs_module_name() + " vtag rtag", cwd = self.template_dir())

	def checkout_project_from_cvs(self, user = None, new_dir_suffix = ""):
		user = user or self.cvs_user
		checkout_path = (self.working_dir() + os.sep + self.clones_folder + os.sep 
			+ self.environment_model.current_username() + os.sep + self.clone_name 
			+ new_dir_suffix)
		self.shell.execute("if not exist " + checkout_path + " mkdir " + checkout_path)
		assert path.exists(self.full_clone_path() + new_dir_suffix)
		self.shell.execute("cvs -d " + self.cvs_url(user) + " checkout -d " 
			+ checkout_path + " " + self.cvs_module_name() , cwd = self.working_dir())

	def update_eclipse_project_file(self, file_path = None):
		file_path = file_path or os.path.join(self.full_clone_path(), ".project")
		xpath = "./name"
		name_element = XmlUtils.updateElementText(
			  file_path = file_path
			, element_xpath = xpath
			, new_value = self.clone_name
		)
		actual = XmlUtils.getElement(file_path, xpath)
		assert(actual.text == self.clone_name
			, "not equal {0} != {1}".format(actual.text, self.clone_name))


	def update_power_tools_xml(self, pt_xml_path = None, model_id = None, is_sub_project = False):
		model_id = model_id or self.clone_name
		pt_xml_path = pt_xml_path or self.template_dir() + sep + "\powertools\powertools.xml"
		assert path.exists(pt_xml_path), "Path not found: " + pt_xml_path
		XmlUtils.updateElementAttributeValue(
			  file_path = pt_xml_path
			, element_xpath = "./property[@name='modelID']"
			, attribute = "value"
			, new_value = model_id
		)
		if is_sub_project:
			XmlUtils.updateElementAttributeValue(
				  file_path = pt_xml_path
				, element_xpath = "./property[@name='subProject']"
				, attribute = "value"
				, new_value = str(is_sub_project)
			)
		#verify the new values were replaced properly
		file = open(pt_xml_path)
		file_contents = file.read()
		file.close()
		new_model_tag = 'property name="modelID" value="' + model_id
		assert new_model_tag in file_contents, ("pattern " + new_model_tag 
		+ " not found in " + file_contents)
		if is_sub_project:
			sub_project_tag = 'property name="subProject" value="' + str(is_sub_project)
			assert new_model_tag in file_contents, ("pattern " + sub_project_tag 
				+ " not found in " + file_contents)

	def delete_clone(self):
		self.shell.execute("rm -rf " + self.full_clone_path())
		self.config.current_project_path = None
		assert path.exists(self.full_clone_path()) == False

	def delete_all_clones(self):
		self.delete_all_local_clones()
		self.delete_all_remote_clones()

	def delete_all_local_clones(self):
		self.shell.execute("rm -rf " + self.dest_dir())
		self.config.current_project_path = None
		assert path.exists(self.dest_dir()) == False, self.dest_dir() + " still exists"

	def delete_all_remote_clones(self):
		self.shell.execute("ssh " + self.cvs_server + " rm -rf " + self.cvs_repo + nix_sep 
			+  self.clones_folder + nix_sep + self.environment_model.current_username())
	
	def cvs_module_name(self, new_dir = None):
		new_dir = new_dir or self.clone_name
		return (self.clones_folder + nix_sep + self.environment_model.current_username() 
			+ nix_sep + new_dir)

	def cvs_url(self, user = None):
		user = user or self.cvs_user
		return ":ext:" + user + "@" + self.cvs_server + ":" + self.cvs_repo

	def dest_dir(self):
		return self.working_dir() + sep + self.clones_folder
	
	def full_clone_path(self):
		return (self.dest_dir() + sep + self.environment_model.current_username() 
			+ sep + self.clone_name)

	def template_dir(self):
		return self.environment_model.cust_demo_path()

	def working_dir(self):
		dirs = self.template_dir().split(sep)
		del dirs[len(dirs)-1]
		return sep.join(dirs)

	def load_cvs_settings_from_current_project_path(self, sub_dir = "CVS"):
		current_project = self.config.current_project_path
		if(current_project is not None):
			print "loading cvs settings from " + current_project
			cvs_dir = os.path.join(current_project, sub_dir)
			self.parse_repo_file(cvs_dir)
			self.parse_root_file(cvs_dir)

	def parse_repo_file(self, cvs_dir):
		repo_file_contents = self.read_file_contents(os.path.join(cvs_dir, "Repository"))
		repository_path_parts = repo_file_contents.split("/")
		self.clones_folder = repository_path_parts[0]
		self.clone_name = repository_path_parts[2]

	def parse_root_file(self, cvs_dir):
		root_file_contents = self.read_file_contents(os.path.join(cvs_dir, "Root"))
		url_parts = root_file_contents.split(":")
		protocol = url_parts[1]
		if protocol != "ext":
			raise Exception("protocol " + protocol + " not supported.")
		user_and_server = url_parts[2].split("@")
		self.cvs_user = user_and_server[0]
		self.cvs_server = user_and_server[1]
		self.cvs_repo = url_parts[3]

	def read_file_contents(self, file_path):
		file_contents = ""
		with open(file_path, "r+") as file_handle:
			file_contents = file_handle.read().strip()
			file_handle.close()
			return file_contents

	def create_sub_project(self, branch_suffix = None, main_project_path = None):
		branch_suffix = branch_suffix or str(uuid.uuid4())
		branch_name = "branch_" + self.clone_name + "_" + branch_suffix
		main_project_path = main_project_path or self.full_clone_path()
		tag_name = "tag_" + branch_name + "_0"
		base_path = os.path.join(self.working_dir(), self.clones_folder
			, self.environment_model.current_username())
		#cvs tag branchname_0
		self.shell.execute("cvs -d " + self.cvs_url() + " tag " + tag_name
			, cwd = main_project_path)
		#cvs tag -r branchname_0 -b branch_name
		self.shell.execute("cvs -d " + self.cvs_url() + " tag -r " + tag_name + " -b " + branch_name
			, cwd = main_project_path)
		#cvs co -r branch_name module_name
		command = ("cvs -d " + self.cvs_url() 
			+ " co -d " + branch_name 
			+ " -r " + branch_name 
			+ " " + self.cvs_module_name())
		self.shell.execute(command, cwd = os.path.join(main_project_path, ".."))
		#update powertools xml
		branch_pt_xml_path = os.path.join(base_path, branch_name, "powertools", "powertools.xml")
		self.update_power_tools_xml(
			pt_xml_path = branch_pt_xml_path
			, model_id = branch_name
			, is_sub_project = True
		)



