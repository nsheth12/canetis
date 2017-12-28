from segment import Segment
from pydub import AudioSegment
from utils import run_gentle, segmentize


def align(audio_file_path, text_file_path):
	# load file
	audio_file = AudioSegment.from_file(audio_file_path)

	# load transcript
	with open(text_file_path, "r") as text_file:
<<<<<<< HEAD
		transcript = text_file.read()
=======
		transcript = text_file.readlines()[0]
>>>>>>> 02984fe734fdbf619458743e14d5ad4a46874f99

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

	# for seg in segs:
	#	print(seg.start_audio, seg.end_audio, seg.aligned)

	res = []

<<<<<<< HEAD
=======
	# set it if its less than the min anchor length
	# if len(segs) < anchor_length : 

	res = []

>>>>>>> 02984fe734fdbf619458743e14d5ad4a46874f99
	# loop through each segment
	for seg in segs:
		if seg.aligned:
			# if aligned --> add to res as is
			res.append(seg)
<<<<<<< HEAD
		#  there is no improvement in alignment --> add unaligned to res as is
=======

		# there is no improvement in alignment --> add unaligned to res as is
>>>>>>> 02984fe734fdbf619458743e14d5ad4a46874f99
		elif len(seg.gentle) == seg.parent_seg_len:	
			res.append(seg)
		# if there is no space between anchor points, discard unaligned seg
		elif (seg.end_audio - seg.start_audio) < .001:
			# need to revisit this
			res.append(seg)
		else:
			# else add run recursion through recurse(Gentle(segment))
			res.extend(recurse(run_gentle(seg, seg.get_text()),
				audio_file, anchor_length=anchor_length))

	return res


<<<<<<< HEAD
# Set up test
audio_file_path = "/Users/nihar/Nihar/SAIL/sample_alignment_data/obama_interview_audio.mp3"
text_file_path = "/Users/nihar/Nihar/SAIL/sample_alignment_data/obama_interview_transcript.txt"
=======


# Set up test
audio_file = "/home/kian/ML/SAIL/sail-forensic-gentle/gentle/examples/data/lucier.mp3"
text_file = "/home/kian/ML/SAIL/sail-forensic-gentle/gentle/examples/data/lucier.txt"
>>>>>>> 02984fe734fdbf619458743e14d5ad4a46874f99

result = align(audio_file, text_file)

for seg in result:
	words = seg.gentle
	for word in words:
		print(word.word, word.start, word.end, word.success())
