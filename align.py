import sys
sys.path.append("/Users/nihar/Nihar/SAIL/gentle")
sys.path.append("/Users/nihar/Nihar/SAIL/gentle/gentle")
sys.path.append("/home/kian/ML/SAIL/sail-forensic-gentle/gentle")
sys.path.append("/home/kian/ML/SAIL/sail-forensic-gentle/gentle/gentle")

from segment import Segment
from pydub import AudioSegment
reload(sys)
sys.setdefaultencoding('utf-8')

from utils import run_gentle, segmentize, fix_unaligned


def align(audio_file_path, text_file_path):
	# load file
	audio = AudioSegment.from_file(audio_file_path)

	#load transcript
	with open(text_file_path, "r") as text_file:
		transcript = text_file.readlines()

	#store audio as a seg and run gentle
	audio_segment = Segment(0, len(audio), [], True, audio, None)
	gentle_output = run_gentle(seg, transcript)

	result = recurse(gentle_output, audio, anchor_length=3)

	return result





segs = segmentize(words, "/home/kian/ML/SAIL/sail-forensic-gentle/gentle/examples/data/lucier.mp3")

	# run gentle and get output dictionary

	# run recursion and set output equal to result array
	# return result array 
	


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

		# if there is no improvement in alignment, give up on recurse 
		# and add the unaligned segment
		elif len(seg.gentle) == seg.parent_seg_len:	
			res.append(seg)

		else:
			# else add run recursion through recurse(Gentle(segment))
			res.append(recurse(run_gentle(seg, seg.get_text()), audio_file, anchor_length=anchor_length))

	return res
