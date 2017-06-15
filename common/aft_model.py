from os import path

class AftModel:

	def libs_dir(self):
		return path.join(self.project_root(), "test/sikuli/libs")

	def project_root(self):
		return path.realpath(path.join(path.dirname(path.realpath(__file__)), "../../.."))

	def src_dir(self):
		return path.join(self.project_root(), "src")

	def assets_dir(self):
		return path.join(self.src_dir(), "assets")

	def images_dir(self):
		return path.join(self.assets_dir(), "images")
