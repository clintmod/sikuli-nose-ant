from sikuli import *
import os
import __builtin__
from utils import Shell
from environment_model import EnvironmentModel
from aft_model import AftModel

model = AftModel()

output_dir_name = "generated_images"
output_dir = os.path.join(
	os.path.join(os.path.dirname(__file__), output_dir_name + ".sikuli")
)

if not os.path.exists(output_dir):
	os.mkdir(output_dir)

python_file = os.path.join(output_dir, output_dir_name + ".py")

if not os.path.exists(python_file):
	open(python_file , 'ab', 0).close()
	with open(python_file, "a") as myfile:
		myfile.write('Do not import this file into your python code.\n')
		myfile.write('It is only meant to be used to examine generated images in the Sikuli IDE.\n')
addImagePath(output_dir)

class FlexTextImageGenerator:

	def __init__(self):
		self.shell = Shell(verbose = True)
		self.environment_model = EnvironmentModel()
		self.aft_model = AftModel()

	def adl_path(self):
		return self.environment_model.flex_home() + r'/bin/adl'

	def flex_image_generator_path(self):
		return self.aft_model.libs_dir() + r"/air/FlexTextImageGenerator-app.xml"

	def command_string(self):
		return '"' + self.adl_path() + '" ' + self.flex_image_generator_path()

	def generate(self, find_options):
		image_name = find_options.image_name()
		
		if(image_name not in open(python_file).read()):
			with open(python_file, "a") as myfile:
				myfile.write(image_name + ' = "' + image_name +'"\n')

		if(os.path.exists(find_options.output_image_path())):
			return image_name

		command = self.command_string() + " -- " + find_options.to_command_line_string()
		self.shell.execute(command)
		return image_name

class TextFindOptions:

	def __init__(self, text = None, font_size = None, font_color = None
			, font_weight = None, background_color = None
			, control_type = "Label", text_align = "left"):
		self.text = text or "NotSet"
		self.font_size = font_size or 11
		self.font_color = font_color or "000000" #black
		self.font_weight = font_weight or "normal"
		self._background_color = background_color
		self.control_type = control_type
		self.text_align = text_align or "left"

	def output_image_path(self):
		return os.path.join(output_dir, self.image_name())

	def image_name(self):
		return (self.text 
			+ "_" + self.font_color 
			+ "_" + self.font_weight 
			+ "_" + str(self.font_size)
			+ "_" + self.background_color
			+ "_" + self.text_align
			+ "_" + self.control_type
			+ ".png"
		)

	@property 
	def background_color(self):
		if(self._background_color is not None):
			return self._background_color
		elif(self.font_color == "FFFFFF"):
			return "000000"
		else:
			return "FFFFFF"

	@background_color.setter
	def background_color(self, value):
		self._background_color = value;

	def to_command_line_string(self):
		if __builtin__.type(self.font_color) is not str:
			raise TypeError("font_color was not a string")

		if __builtin__.type(self.background_color) is not str:
			raise TypeError("background_color was not a string")

		return_val = '-type={0} -text="{1}" -fontSize={2} -fontColor={3} -fontWeight={4} -backgroundColor={5} -outputImagePath="{6}" -textAlign="{7}"'.format(
			self.control_type, self.text, self.font_size, self.font_color
			, self.font_weight, self.background_color, self.output_image_path()
			, self.text_align
		)
		return return_val

class ImageFindOptions:

	def __init__(self, input_image_name, background_color = None
		, height = None, width = None):
		if input_image_name is None:
			raise ValueError("input_image_name cannot be None")
		self.aft_model = AftModel()
		self.input_image_name = input_image_name
		if not os.path.exists(self.input_image_path()):
			raise ValueError("input image does not exist at:" + self.input_image_path())
		self.background_color = background_color or "FFFFFF"
		self.height = height
		self.width = width
		
	def image_name(self):
		parts = self.input_image_name.split(".")
		del parts[-1]
		name_without_extension = ".".join(parts)
		return name_without_extension + "_" + self.background_color + ".png"

	def output_image_path(self):
		return os.path.join(output_dir, self.image_name())

	def input_image_path(self):
		return os.path.join(self.aft_model.images_dir(), self.input_image_name)

	def to_command_line_string(self):
		if __builtin__.type(self.background_color) is not str:
			raise TypeError("background_color was not a string")

		return_val = '-type=Image -imagePath="{0}" -backgroundColor={1} -outputImagePath="{2}"'.format(
			self.input_image_path(), self.background_color, self.output_image_path()
		)

		if self.height is not None:
			return_val += " -height={0}".format(self.height)
		
		if self.width is not None:
			return_val += " -width={0}".format(self.width)

		return return_val

generator = FlexTextImageGenerator()



def flex_label(text, font_size = None, font_color = None
			, font_weight = None, background_color = None, text_align = None):
	find_options = TextFindOptions(text = text, font_size = font_size, 
		font_color = font_color, font_weight = font_weight
		, background_color = background_color, control_type = "Label"
		, text_align=text_align)
	return generator.generate(find_options)

def flex_button(text, font_size = None, font_color = None
			, font_weight = None, background_color = None, text_align = None):
	find_options = TextFindOptions(text = text, font_size = font_size, 
		font_color = font_color, font_weight = font_weight, 
		background_color = background_color, control_type = "Button"
		, text_align=text_align)
	return generator.generate(find_options)

def flex_image(input_image_name = None, background_color = None, height = None
					, width = None):
	find_options = ImageFindOptions(input_image_name = input_image_name, background_color = background_color
									, height = height, width = width)
	return generator.generate(find_options)
	