


class Segment(Object):
	"""
	Class to store start/end values 
	of an audio file relative to the overall file
	during a recursive call"""
	
	def __init__(self, initial_start_audio, initial_end_audio, gentle_output, aligned):
		"""Initialize start audio to be the start of the segment
		being recursively called, then update that value"""
		self.start_audio = initial_start_audio
		self.end_audio = initial_end_audioj
		self.gentle = gentle_output
		self.aligned = aligned
	
	def get_text(self):
		"""get the text to pass
		into gentle from the dictionary
		values of gentle"""
		pass
	
	
