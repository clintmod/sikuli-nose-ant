import os
from sikuli import *
import unittest
import test_utils
from search import flex_image, flex_label, flex_button, FlexTextImageGenerator, TextFindOptions, ImageFindOptions
from nose.plugins.attrib import attr

@attr("slow", "search", "search_aft")
class SearchTest(unittest.TestCase):
	
	app = None

	@classmethod
	def setUpClass(cls):
		test_files_path = os.path.join(os.path.dirname(__file__), 'testfiles', 'images')
		test_file_path = os.path.join(test_files_path, "list_test.png")
		global app 
		app = App.open("mspaint " + test_file_path)
		wait(2)

	@classmethod
	def tearDownClass(cls):
		app.close()

	def setUp(self):
		test_utils.skip_if_group_failed_or_skipped("unit")
	
	def tearDown(self):
		pass

	def test_flex_label_works(self):
		region = find(flex_label(text = "Pay Plans"))
		self.assertIsNotNone(region)

	def test_flex_label_works_with_font_options(self):
		region = find(flex_label(text = "Select Configurable Areas"
			, font_weight = "bold"
			, font_color = "FFFFFF"
			, font_size = 14
			, background_color = "7E9CBB"
		))
		self.assertIsNotNone(region)

	def test_flex_label_works_with_project_text_white(self):
		region = find(flex_label(
			text = "Project", font_color = "FFFFFF"
			, font_size = 11, font_weight = "normal"
		))
		self.assertIsNotNone(region)

	def test_flex_button_works(self):
		region = find(flex_button(
			text = "Cancel", font_weight = "bold", background_color = "C1D4E3"
		))
		self.assertIsNotNone(region)

	def test_flex_image_works_with_Common_image(self):
		region = find(flex_image(
			  input_image_name = "Common.png", background_color = "000000"
		))
		self.assertIsNotNone(region)

	def test_flex_image_works_with_Project_image(self):
		region = find(flex_image(
			 input_image_name = "Project.png"
			 ,background_color = "000000"
		))
		self.assertIsNotNone(region)


@attr("unit", "search", "image_generator")
class FlexTextImageGeneratorTest(unittest.TestCase):

	def setUp(self):
		self.sut = FlexTextImageGenerator()
	
	def tearDown(self):
		pass

	def test_generate_works_with_TextFindOptions(self):
		find_options = TextFindOptions()
		self.sut.generate(find_options);
		self.assert_path_works(find_options.output_image_path())

	def test_generate_works_with_ImageFindOptions(self):
		find_options = ImageFindOptions(input_image_name = "Project.png", height = 20, width = 20)
		self.sut.generate(find_options);
		self.assert_path_works(find_options.output_image_path())

	def test_adl_path_works(self):
		self.assert_path_works(self.sut.adl_path())

	def test_flex_image_generator_path_works(self):
		self.assert_path_works(self.sut.flex_image_generator_path())

	def assert_path_works(self, path):
		self.assertIsNotNone(path)
		assert os.path.exists(path), path + " does not exist."


@attr("unit", "search", "text_find_options")
class TextFindOptionsTest(unittest.TestCase):

	def setUp(self):
		self.sut = TextFindOptions()
	
	def tearDown(self):
		pass

	def test_constructor_defaults_background_color_to_black_for_white_text(self):
		self.sut = TextFindOptions(font_color = "FFFFFF")
		self.assertEqual("000000", self.sut.background_color)


@attr("unit", "search", "image_find_options")
class ImageFindOptionsTest(unittest.TestCase):

	def setUp(self):
		self.sut = ImageFindOptions("Project.png")
	
	def tearDown(self):
		pass

	def test_output_image_path_works(self):
		self.sut.input_image_name = "asdf.png"
		actual = self.sut.output_image_path()
		assert "asdf" in actual