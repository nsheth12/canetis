
class Segment(object):
	"""
	Class to store start/end values 
	of an audio file relative to the overall file
	during a recursive call"""
	
	def __init__(self, initial_start_audio, initial_end_audio, gentle_output, aligned):
		"""Initialize start audio to be the start of the segment
		being recursively called, then update that value"""
		self.start_audio = initial_start_audio
		self.end_audio = initial_end_audio
		self.gentle = gentle_output
		self.aligned = aligned
	
	def get_text(self):
		"""get the text to pass
		into gentle from the dictionary
		values of gentle"""
		text = []
		for info in self.gentle:
			text.append(info["word"])
		return text		

#quick test

test_output = [ {"case": "success", "word":"a"}, {"case": "success", "word":"b"}, {"case": "success", "word":"c"}, {"case": "success", "word":"d"}, {"case": "success", "word":"e"}]

s = Segment(0, 12, test_output, False)
#print(s.get_text())

