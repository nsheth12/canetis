import Segment

def gentle (s):
	"""
	takes in a segment
	1. create new text file containing text
	2. create new audio with librosa
	3. run Gentle with these two
	4. delete text file/audio files
	"""

def segmentize (gentle_outputs, anchor_length=3):
	"""
	takes in Gentle output (array of dicts)
	break into segments which marked as aligned or unaligned
	"""

	#tracks number of correct in a row to check if anchor
	correct_count = 0

	#stores index of first correct point in a series
	first_correct_index = None

	#store all segments
	segs = []

	#run through the list of gentle output dictionaries
	for index, output in enumerate(gentle_outputs):
		
		#if the aligner works
		if output["case"] == "success":
			#update variable values and move on
			
			if !first_correct_index:
				first_correct_index = index				
		#if aligner doesn't work
		else:
			#check if there are enough correct for an achor
			if correct_count >= anchor_length:
				#store the previous unaligned segments as a seg- append
				
				#remove previous unaligned segments

				#store anchor as a seg
				
				#remove anchor

			#reset counter variables




			
	

