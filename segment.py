


class Segment(Object):
	def __init__(self, initial_start_audio, initial_end_audio, gentle_output):
		"""Initialize start audio to be the start of the segment
		being recursively called, then update that value"""
		self.start_audio = initial_start_audio
		self.end_audio = initial_end_audioj
		self.gentle = gentle_output
	
	def get_text(self):
		pass
	
	
