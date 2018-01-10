from segment import Segment
from pydub import AudioSegment
from utils import run_gentle, get_counts
from segmentizer import segmentize 


def align(audio_file_path, text_file_path, anchor_length=15):

	# load file
	audio_file = AudioSegment.from_file(audio_file_path)

	# load transcript
	with open(text_file_path, "r") as text_file:
		transcript = text_file.read()



	#store audio as a seg and run gentle
	audio_segment = Segment(0, len(audio_file), [], True, audio_file, None)
#	print(transcript)
	gentle_output = run_gentle(audio_segment, transcript)

	get_counts(gentle_output) 
	
		
	#print(len(gentle_output))
	#run Moreno's algorithm on initial gentle output
	result = recurse(gentle_output, audio_file, anchor_length=anchor_length)

	# return result of Moreno's algorithm
	return result


def recurse(gentle_output, audio_file, anchor_length=15):
	# if % unaligned in gentle_output < 5%, return gentle output
	# call segmentize on gentle_output, getting list of segments
	segs = segmentize(gentle_output, audio_file, anchor_length=anchor_length)


	res = []

	# loop through each segment
	for seg in segs:
		if seg.aligned:
			# if aligned --> add to res as is
			#print(seg.start_audio, seg.end_audio, seg.aligned, seg.get_text())
			res.append(seg)
		#  there is no improvement in alignment --> add unaligned to res as is
		elif len(seg.gentle) == seg.parent_seg_len:
			#print(seg.start_audio, seg.end_audio, seg.aligned, seg.get_text())	
			res.append(seg)
		# if there is no space between anchor points, discard unaligned seg
		elif (seg.end_audio - seg.start_audio) < .001:
			#print(seg.start_audio, seg.end_audio, seg.aligned, seg.get_text())
			# need to revisit this
			res.append(seg)
		else:
			#print('passed pdb')

			# else add run recursion through recurse(Gentle(segment))
			res.extend(recurse(run_gentle(seg, seg.get_text()),
				audio_file, anchor_length=anchor_length))

	return res


