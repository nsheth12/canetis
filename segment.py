
class Segment(object):
	"""
	Class to store start/end values 
	of an audio file relative to the overall file
	during a recursive call"""
	
	def __init__(self, start_audio, end_audio, gentle_output, aligned, audio_file):
		"""Initialize start audio to be the start of the segment
		being recursively called, then update that value"""
		self.start_audio = start_audio
		self.end_audio = end_audio
		self.gentle = gentle_output
		self.aligned = aligned
		self.audio_file = audio_file
	
	def get_text(self):
		"""get the text to pass
		into gentle from the dictionary
		values of gentle"""
		text = []
		for info in self.gentle:
			text.append(info["word"])
		return text
