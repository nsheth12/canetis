from segment import Segment
from utils import *
import librosa



def align(audio_file, text_file, error_rate=.05):
	# get audio and text files
	# run gentle and get output dictionary
	# run recursion and set output equal to result array
	# return result array 


def recurse(gentle_output, audio_file_maybe_path, error_rate):
	# if % unaligned in gentle_output < 5%, return gentle output
	# call segmentize on gentle_output, getting list of segments
	res = []
	# loop through each segment
	#	if aligned --> add to res as is
	#	else add recurse(Gentle(segment))
	return res
