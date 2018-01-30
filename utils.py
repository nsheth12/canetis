import os
import gentle as gentle


def run_gentle(seg, transcript):
    """
    Takes in a segment
    1. create new text file containing text
    2. create new audio with pydub
    3. run Gentle with these two
    4. delete text file/audio files

    Parameters
    ---------
    seg : Segment object to align with Gentle
    transript : string holding the relevant transcript for this segment
    """
    audio_cut = seg.audio_file[1000 * seg.start_audio : 1000 * seg.end_audio]

    audio_cut.export("temp_audio.wav", format="wav")

    # run Gentle
    resources = gentle.Resources()
    with gentle.resampled("temp_audio.wav") as wavfile:
        aligner = gentle.ForcedAligner(resources, transcript)
        result = aligner.transcribe(wavfile).words

    # delete cut audio file
    os.remove("temp_audio.wav")

    # fix unaligned-word start/end time data
    fix_unaligned(result, len(audio_cut) / 1000)

    # put gentle timestamps in relation to entire file
    for word in result:
        word.start += seg.start_audio
        word.end += seg.start_audio

    return result


def fix_unaligned(gentle_output, audio_file_length):
    """
    Give approximate start/end times to unaligned words in the Gentle output.

    Parameters
    ----------
    gentle_output : list of Word objects returned by Gentle
    audio_file : AudioSegment object representing the entire audio file
    """

    initial_start = 0

    for word in gentle_output:
        if not word.success():
            word.start = initial_start
        else:
            initial_start = word.end

    initial_end = audio_file_length

    for word in gentle_output[::-1]:
        if not word.success():
            word.end = initial_end
        else:
            initial_end = word.start



def print_results(result):
    """
    Helper function that prints
    the results of align. 

    Parameters
    -----------------------
    List of segment Objects
    
    Outputs
    ------------------
    Prints each word, its start
    time, end time and whether it has 
    been aligned or not
    """

    for seg in result:
        words = seg.gentle
        print("Format: (Word, Start-Time, End-Time, Aligned-Unaligned)")
        for word in words:
            print_str = "('" + word.word + "',"
            print_str += " aligned, " if word.success() else " not aligned, "
            if word.success():
                print_str +=  str(word.start)
                print_str += ", " + str(word.end) + ")"
            print(print_str)

        print("Format: (Word, Aligned/Unaligned, Start-Time, End-Time)")
