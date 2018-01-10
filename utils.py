import os
from segment import Segment
from pydub import AudioSegment

import sys
#add path to gentle directory and gentle code directory
sys.path.append("/Users/nihar/Nihar/SAIL/gentle")
sys.path.append("/Users/nihar/Nihar/SAIL/gentle/gentle")
sys.path.append("/home/kian/ML/SAIL/sail-forensic-gentle/gentle")
sys.path.append("/home/kian/ML/SAIL/sail-forensic-gentle/gentle/gentle")
sys.path.insert(0,"/home/coder/Desktop/alignment_nihar_kian/gentle")
sys.path.insert(0, "/home/coder/Desktop/alignment_nihar_kian/gentle/gentle")

import gentle as gentle


def run_gentle(seg, transcript):
	"""
	takes in a segment
	1. create new text file containing text
	2. create new audio with pydub
	3. run Gentle with these two
	4. delete text file/audio files
	"""
	# I think they are wav files, but not sure
	audio_cut = seg.audio_file[1000 * seg.start_audio : 1000 * seg.end_audio]

	# print("Audio Len", len(audio_cut))
	
	audio_cut.export("temp_audio.wav", format="wav")


	# run Gentle
	resources = gentle.Resources()
	with gentle.resampled("temp_audio.wav") as wavfile:
		aligner = gentle.ForcedAligner(resources, transcript)
		result = aligner.transcribe(wavfile).words

	# delete cut audio file
	os.remove("temp_audio.wav")
	
	
	#fix unaligned-word start/end time data
	fix_unaligned(result, len(audio_cut)/1000)

	#put gentle timestamps in relation to entire file
	for word in result:	
		word.start += seg.start_audio
		word.end += seg.start_audio

	return result



def fix_unaligned (gentle_output, audio_file_length):
	"""
	Give approximate start/end times to unaligned words in the Gentle output.

	Parameters
	----------
	gentle_output: list of Word objects returned by Gentle
	audio_file: AudioSegment object representing the entire audio file
	"""

	initialStart = 0

	for word in gentle_output:
		if not word.success():
			word.start = initialStart
		else:
			initialStart = word.end

	initialEnd = audio_file_length

	for word in gentle_output[::-1]:
		if not word.success():
			word.end = initialEnd
		else:
			initialEnd = word.start
			

def get_counts(gentle_output):

 	words_aligned = 0
	total_count = 0
	for word in gentle_output:
		if word.success():
			words_aligned+=1
		total_count+=1

	print("Gentle's words aligned:", words_aligned)
	print("Gentle's Total Count:", total_count)