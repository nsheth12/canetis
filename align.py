from segment import Segment
from pydub import AudioSegment
from utils import run_gentle, segmentize


def align(audio_file_path, text_file_path):
	# load file
	audio_file = AudioSegment.from_file(audio_file_path)

	#load transcript
	with open(text_file_path, "r") as text_file:
		transcript = text_file.readlines()

	#store audio as a seg and run gentle
	audio_segment = Segment(0, len(audio_file), [], True, audio_file, None)
	gentle_output = run_gentle(audio_segment, transcript)

	#run Moreno's algorithm on initial gentle output
	result = recurse(gentle_output, audio_file, anchor_length=3)


	#return result of Moreno's algorithm
	return result

	


def recurse(gentle_output, audio_file, anchor_length=3):

	# if % unaligned in gentle_output < 5%, return gentle output
	# call segmentize on gentle_output, getting list of segments
	segs = segmentize(gentle_output, audio_file, anchor_length=anchor_length)

	res = []

	#set it if its less than the min anchor length
	#if len(segs) < anchor_length : 
	#	return segs

	res = []
	# loop through each segment
	for seg in segs:
		if seg.aligned:

			# if aligned --> add to res as is
			res.append(seg)

		#  there is no improvement in alignment --> add unaligned to res as is
		elif len(seg.gentle) == seg.parent_seg_len:	
			res.append(seg)

		else:
			# else add run recursion through recurse(Gentle(segment))
			res.append(recurse(run_gentle(seg, seg.get_text()),
			audio_file, anchor_length=anchor_length))

	return res
