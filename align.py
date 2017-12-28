from utils import run_gentle, segmentize

def align(audio_filename, text_file):
	# get audio and text files

	# run gentle and get output dictionary
	# run recursion and set output equal to result array
	# return result array 
	pass


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

		#if there is no improvement in alignment, add the seg
		elif len(seg.gentle) == seg.parent_seg_len:
			res.append(seg)
		else:
			# else add recurse(Gentle(segment))
			res.append(recurse(run_gentle(seg), audio_file, anchor_length=anchor_length))

	return res
