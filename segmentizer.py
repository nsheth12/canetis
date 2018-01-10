
from segment import Segment


def segmentize (gentle_outputs, audio_file, 
				anchor_length, rel_audio_start=0):
	"""
	takes in Gentle output (list of Word objects)
	Converts the list storing each word into a
    list of Segment Objects in order to break up
    Gentle's output into Anchor Points and recursive points.

    Anchor Point is defined as a set of consecutively aligned
    words whose length is greater than the defined anchor length
	"""

    # variables to help with bounding Segments
    correct_count = 0
    end_prev_anchor = 0
    first_correct_index = None

    # convenience variable 
    total_gentle_len = len(gentle_outputs)

	# Array to store all segments
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



def get_segment (gentle_output, rel_audio_start, aligned, audio_file, total_gentle_len):
	# relative audio start time plus the audio time of the first/last word
	audio_start = rel_audio_start + gentle_output[0].start
	audio_finish = rel_audio_start + gentle_output[-1].end

	seg = Segment(audio_start, audio_finish,
				  gentle_output, aligned, audio_file,
				  total_gentle_len)
	
	return seg
