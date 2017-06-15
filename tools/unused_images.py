import sys
import os
import os.path

if len(sys.argv) < 4:
	sys.exit("missing arguments - e.g. " + __file__ + " c:\images c:\srcdir False")

images_dir = sys.argv[1]
src_dir = sys.argv[2]
should_delete = sys.argv[3]

all_images = []
used_images = []
unused_images = []

def collect_all_images():
	for dirpath, dirnames, filenames in os.walk(images_dir):
		for filename in [f for f in filenames if f.endswith(".png")]:
			all_images.append(filename)

def collect_unused_images():
	global unused_images
	unused_images = all_images[:]
	for dirpath, dirnames, filenames in os.walk(src_dir):
		for filename in [f for f in filenames if f.endswith(".mxml") or f.endswith(".as") or f.endswith(".css")]:
			print "searching " + os.path.join(dirpath, filename)
			file_contents = open(os.path.join(dirpath, filename)).read().lower()
			for image_name in all_images:
				if image_name.lower() in file_contents:
					print "found " + image_name
					if image_name not in used_images:
						used_images.append(image_name)
					while image_name in unused_images: 
						unused_images.remove(image_name)    


def list_unused_images():
	collect_all_images()
	collect_unused_images()
	print "\n"
	print "all_images length = {0}".format(len(all_images))
	print "unused_images length = {0}".format(len(unused_images))
	print "used_images length = {0}".format(len(used_images))

def delete_unused_images():
	print "deleting"
	print "unused_images length = {0}".format(len(unused_images))
	for image_name in unused_images:
		image_path = os.path.join(images_dir, image_name)
		print "deleting " + image_path
		os.remove(image_path)

list_unused_images()

if(should_delete == "True"):
	delete_unused_images()