from sikuli import *
import images

HORIZONTAL = "HORIZONTAL"
VERTICAL = "VERTICAL"

class Scroller(object):

	def scroll_to(self, pattern_to_find = None, direction = None, pixels_to_scroll = 100
			, region = None, thumb = None, time_out = 300, thumb_timeout = 30):
		if pattern_to_find is None:
			raise ValueError("pattern_to_find can not be None")
		if direction is None:
			direction = VERTICAL
		pixels_to_scroll = pixels_to_scroll or 100
		thumb = thumb or images.vertical_scroll_thumb
		exists_func = exists
		find_func = find
		if region is not None:
			exists_func = region.exists
			find_func = region.find
		timeout_timer = ScrollTimeOutTimer(time_out)
		while(exists_func(pattern_to_find, 0.1) == None):
			if timeout_timer.timed_out():
				message = "Pattern {0} was not found while scrolling in {1} seconds."
				raise TimeoutException(message.format(pattern_to_find, time_out))
			if exists_func(thumb, thumb_timeout) == None:
				raise ScrollThumbNotFoundException(direction)
			thumb_region = find_func(thumb)
			location = self.get_scroll_to_location(thumb_region, direction, pixels_to_scroll)
			dragDrop(thumb_region, location)
		
		if exists_func(pattern_to_find) is not None:
			return find_func(pattern_to_find)
		else:
			return None

	def get_scroll_to_location(self, thumb_region, direction, pixels_to_scroll = 10):
		if thumb_region is None:
			raise ValueError("thumb_region can not be None")
		if direction == VERTICAL:
			return Location(thumb_region.x, thumb_region.y + pixels_to_scroll)
		elif direction == HORIZONTAL:
			return Location(thumb_region.x + pixels_to_scroll, thumb_region.y)
		else:
			raise ValueError("unknown direction " + str(direction))

	def reset():
		pass

class VScroller(Scroller):
	
	def scroll_to(self, pattern_to_find, pixels_to_scroll = 100, region = None, time_out = 300):
		return super(VScroller, self).scroll_to(
			pattern_to_find = pattern_to_find
			, direction = VERTICAL
			, pixels_to_scroll = pixels_to_scroll
			, region = region
			, thumb = images.vertical_scroll_thumb
			, time_out = time_out
		)

class HScroller(Scroller):
	
	def scroll_to(self, pattern_to_find, pixels_to_scroll = 100, region = None, time_out = 300):
		return super(HScroller, self).scroll_to(
			pattern_to_find = pattern_to_find
			, direction = HORIZONTAL
			, pixels_to_scroll = pixels_to_scroll
			, region = region
			, thumb = images.horizontal_scroll_thumb
			, time_out = time_out
		)


class ScrollTimeOutTimer(object):

	def __init__(self, time_out_in_seconds = 300, current_epoch_seconds = None):
		self.current_epoch_seconds = current_epoch_seconds or time.time()
		self.time_out_in_seconds = time_out_in_seconds or 300
		self.time_out_epoch_seconds = self.current_epoch_seconds + self.time_out_in_seconds
	
	def timed_out(self, current_epoch_seconds = None):
		self.current_epoch_seconds = current_epoch_seconds or time.time()
		print "self.time_out_epoch_seconds = " + str(self.time_out_epoch_seconds)
		print "self.current_epoch_seconds = " + str(current_epoch_seconds)
		if self.current_epoch_seconds >= self.time_out_epoch_seconds:
			return True
		else:
			return False

class TimeoutException(Exception):
	pass

class ScrollThumbNotFoundException(Exception):
	
	def __init__(self, direction):
		super(ScrollThumbNotFoundException, self).__init__(None)
		self.direction = direction

	def __str__(self):
		return self.direction + " scroll thumb not found"