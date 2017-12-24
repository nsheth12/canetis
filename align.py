from utils import gentle, segmentize

def align(audio_file, text_file, error_rate=.05):
	# get audio and text files
	# run gentle and get output dictionary
	# run recursion and set output equal to result array
	# return result array 


def recurse(gentle_output, audio_file_maybe_path, error_rate):
	# if % unaligned in gentle_output < 5%, return gentle output
	# call segmentize on gentle_output, getting list of segments
	segs = segmentize(gentle_output)

	if len(segs) == 1:
		return segs

	res = []
	# loop through each segment
	for seg in segs:
		if seg.aligned:
			# if aligned --> add to res as is
			res.append(seg)
		else:
			# else add recurse(Gentle(segment))
			res.append(recurse(gentle(seg)))

	return res
