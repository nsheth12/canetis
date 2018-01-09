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


def segmentize (gentle_outputs, audio_file, 
				anchor_length=3, rel_audio_start=0):
	"""
	takes in Gentle output (list of Word objects)
	break into segments which marked as aligned or unaligned
	"""

	correct_count = 0
	end_prev_anchor = 0
	total_gentle_len = len(gentle_outputs)

	# stores index of first correct point in a series
	first_correct_index = None

	# store all segments
	segs = []

	# run through the list of Word objects
	for index, word in enumerate(gentle_outputs):
		# if the word was successfully aligned
		if word.success():
			# update variable values and move on
			correct_count += 1
			
			# update first_correct tracker
			if first_correct_index is None:
				first_correct_index = index	


		# if unaligned check if there are enough correct for anchor
		elif correct_count >= anchor_length:
			
			# check if there is an unaligned seg before anchor point
			if end_prev_anchor != first_correct_index:
				# store the previous unanchored segments as a seg and append
				seg = get_segment(gentle_outputs[end_prev_anchor: \
					first_correct_index], rel_audio_start, False, audio_file,
					total_gentle_len)	
				segs.append(seg)

			# store the anchor segment
			seg = get_segment(gentle_outputs[first_correct_index: \
				index], rel_audio_start, True, audio_file,
				total_gentle_len)

			segs.append(seg)	
			
			# update end of prev anchor tracker
			end_prev_anchor = index

			# reset counter variables
			correct_count = 0
			first_correct_index = None

		elif index < len(gentle_outputs) - 1:

			# reset counter variables
			correct_count = 0
			first_correct_index = None
		

		# if we have reached the end of the audio file
		# we need to segmentize all the remaining
		# unsegmented part of the transcript/audiofile
		if index == len(gentle_outputs) - 1:

			# if current seg is an anchor point ...
			if correct_count >= anchor_length:
				
				if end_prev_anchor != first_correct_index:
					# get previous unanchored seg
					seg = get_segment(gentle_outputs[end_prev_anchor: \
						first_correct_index], rel_audio_start, False, audio_file,
						total_gentle_len)	

					# store previous unanchored seg
					segs.append(seg)	

				# get the anchor segment
				seg = get_segment(gentle_outputs[first_correct_index:], \
					rel_audio_start, True, audio_file, total_gentle_len)

				# store the anchor seg
				segs.append(seg)	
				
				# update end of prev anchor tracker
				end_prev_anchor = index
			
			# if current segment does not qualify as an anchor point
			else:
					
				# store the previous unanchored segments as a seg- append
				seg = get_segment(gentle_outputs[end_prev_anchor:], \
					rel_audio_start, False, audio_file, total_gentle_len)	
				segs.append(seg)
		

	return segs


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


def get_segment (gentle_output, rel_audio_start, aligned, audio_file, total_gentle_len):

	# relative audio start time plus the audio time of the first/last word
	audio_start = rel_audio_start + gentle_output[0].start
	audio_finish = rel_audio_start + gentle_output[-1].end

	seg = Segment(audio_start, audio_finish,
				  gentle_output, aligned, audio_file,
				  total_gentle_len)
	
	return seg
