
from segment import Segment


def segmentize(gentle_outputs, audio_file, 
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

    #convenience variable 
    total_gentle_len = len(gentle_outputs)

    # Array to store all final segments
    segs = []

    # run through the list of Word objects
    for index, word in enumerate(gentle_outputs):

        if word.success():

            # if the word was successfully aligned
            # update variable values and move on
            correct_count += 1

            # update first_correct tracker for later bounding
            if first_correct_index is None:
                first_correct_index = index	


        # if word is unaligned, check if current 
        elif correct_count >= anchor_length:
            
            # Make sure that the unaligned segment exists
            # Would throw an error if the audio file began
            #with an anchor point
            if end_prev_anchor != first_correct_index:

                # load the previous unanchored words as a Segment 
                seg = get_segment(gentle_outputs[end_prev_anchor: \
                    first_correct_index], rel_audio_start, False, audio_file,
                    total_gentle_len)	
  
                segs.append(seg)

            # Load the current ancor words as a Segment
            seg = get_segment(gentle_outputs[first_correct_index: \
                index], rel_audio_start, True, audio_file,
                total_gentle_len)

            segs.append(seg)
    
            # set the end prev_anchor tracker 
            # to the current location
            end_prev_anchor = index

            # reset counter variables
            correct_count = 0
            first_correct_index = None

        # Resets counter variables if the
        # current word is unaligned and is less
        # than the anchor length
        elif index < len(gentle_outputs) - 1:
            
            # reset counter variables
            correct_count = 0
            first_correct_index = None
		

        # if we have reached the end of the audio file
        # we need to segmentize all the remaining
        # unsegmented part of the transcript/audiofile
        # and reaccount for all cases
        if index == len(gentle_outputs) - 1:

            # Case: current seg is an anchor point
            # Store unanchored segment 
            # Then store anchored segment
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

            # Case: current segment does not qualify as an anchor point
            # Then just store all the remaining words as an unanchored segment    
            
            else:

                # store the previous unanchored segments as a seg- append
                seg = get_segment(gentle_outputs[end_prev_anchor:], \
                rel_audio_start, False, audio_file, total_gentle_len)	
                segs.append(seg)


    return segs



def get_segment (bounded_gentle_output, rel_audio_start, aligned, audio_file, total_gentle_len):

    """
    Helper function to easily convert a bounded
    portion of gentle output into a Segment
    """

    # relative audio start time plus the audio time of the first/last word
    audio_start = rel_audio_start + bounded_gentle_output[0].start
    audio_finish = rel_audio_start + bounded_gentle_output[-1].end

    seg = Segment(audio_start, audio_finish,
    bounded_gentle_output, aligned, audio_file,
    total_gentle_len)

    return seg
