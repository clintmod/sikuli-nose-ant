import os
import unittest
from aft_model import AftModel

from nose.plugins.attrib import attr

@attr("unit", "aft_model")
class AftModelTest(unittest.TestCase):
	
	def setUp(self):
		self.sut = AftModel()
	
	def tearDown(self):
		pass

	def test_that_libs_dir_works(self):
		libs_dir = self.sut.libs_dir()
		self.assertIsNotNone(libs_dir)
		assert os.path.exists(libs_dir)

	def test_that_project_root_works(self):
		root_dir = self.sut.libs_dir()
		self.assertIsNotNone(root_dir)
		assert os.path.exists(root_dir)

	def test_that_src_dir_works(self):
		src_dir = self.sut.src_dir()
		self.assertIsNotNone(src_dir)
		assert os.path.exists(src_dir)

	def test_that_assets_dir_works(self):
		src_dir = self.sut.src_dir()
		self.assertIsNotNone(src_dir)
		assert os.path.exists(src_dir)

	def test_that_images_dir_works(self):
		src_dir = self.sut.src_dir()
		self.assertIsNotNone(src_dir)
		assert os.path.exists(src_dir)