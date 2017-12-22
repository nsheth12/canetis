import sys
sys.path.append() # put here path to gentle module

from segment import Segment
from pydub import AudioSegment
import os

def gentle (seg, audio_file):
	"""
	takes in a segment
	1. create new text file containing text
	2. create new audio with pydub
	3. run Gentle with these two
	4. delete text file/audio files
	"""
	transcript = " ".join(seg.get_text())

	# I think they are wav files, but not sure
	audio_full = AudioSegment.from_file(audio_file, format="wav")
	audio_cut = audio_full[seg.start_audio:seg.end_audio]
	audio_cut.export("temp_audio.wav", format="wav")

	# run Gentle
	resources = gentle.Resources()
	with gentle.resampled("temp_audio.wav") as wavfile:
		aligner = gentle.ForcedAligner(resources, transcript)
		result = aligner.transcribe(wavfile)

	# delete cut audio file
	os.remove("temp_audio.wav")

	


def segmentize (gentle_outputs, anchor_length=3, rel_audio_start=0):
	"""
	takes in Gentle output (array of dicts)
	break into segments which marked as aligned or unaligned
	"""

	correct_count = 0
	end_prev_anchor = 0

	# stores index of first correct point in a series
	first_correct_index = None

	# store all segments
	segs = []

	# run through the list of gentle output dictionaries
	for index, output in enumerate(gentle_outputs):
	
		
		# if the aligner works
		if output["case"] == "success":

			# update variable values and move on
			correct_count += 1
			
			# update first_correct tracker
			if not first_correct_index:
				first_correct_index = index
				
		#if aligner doesn't work
		
		#check if there are enough correct for an achor
		elif correct_count >= anchor_length:
			
			#store the previous unanchored segments as a seg- append
			seg = get_segment(gentle_outputs[end_prev_anchor:\
			first_correct_index], rel_audio_start, False)	

			segs.append(seg)	
			
			#store the anchor segment
			seg = get_segment(gentle_outputs[first_correct_index:\
			index], rel_audio_start, True)
			segs.append(seg)	
			
			#update end of prev anchor tracker
			end_prev_anchor = index

			#reset counter variables
			correct_count = 0
			first_correct_index = None

			
		if index == len(gentle_outputs)-1:

			

			if correct_count >= anchor_length:

				#store the previous unanchored segments as a seg- append
				seg = get_segment(gentle_outputs[end_prev_anchor:\
				first_correct_index], rel_audio_start, False)	

				segs.append(seg)	
				
				#store the anchor segment
				seg = get_segment(gentle_outputs[first_correct_index:], \
				rel_audio_start, True)
				segs.append(seg)	
				
				# update end of prev anchor tracker
				end_prev_anchor = index
				
			else: 

				#store the previous unanchored segments as a seg- append
				seg = get_segment(gentle_outputs[end_prev_anchor:],\
				rel_audio_start, False)	

				segs.append(seg)

	return segs

def get_segment(gentle_output, rel_audio_start, aligned):
	# relative audio start time plus the audio time of the first/last word
	audio_start = rel_audio_start + gentle_output[0]["audio_start"]
	audio_finish = rel_audio_start + gentle_output[-1]["audio_end"]

	seg = Segment(audio_start, audio_finish, gentle_output, aligned)
	
	return seg


test_output = [ {"case":"success", "word":"a", "audio_start":10}, \
{"case": "fail", "word":"b", "audio_end":17}, \
{"case": "success", "word":"c", "audio_start":10}, \
{"case": "success", "word":"c"}, \
{"case": "success", "word":"c",  "audio_end":19}, \
{"case": "fail", "word":"c", "audio_start":19}, \
{"case": "success", "word":"d"}, \
{"case":"success", "audio_end":20, "word":"d"}]


		
x = segmentize(test_output)

for i in x:
	print(i.get_text())



def update_segs(gentle_outputs, ):
	if correct_count >= anchor_length:

			#store the previous unanchored segments as a seg- append
			seg = get_segment(gentle_outputs[end_prev_anchor:\
			first_correct_index], rel_audio_start, False)	

			segs.append(seg)	
			
			#store the anchor segment
			seg = get_segment(gentle_outputs[first_correct_index:], \
			rel_audio_start, True)
			segs.append(seg)	
			
			# update end of prev anchor tracker
			end_prev_anchor = index
			
		else: 

			#store the previous unanchored segments as a seg- append
			seg = get_segment(gentle_outputs[end_prev_anchor:],\
			rel_audio_start, False)	
			
			segs.append(seg)