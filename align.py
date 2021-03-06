from pydub import AudioSegment
from segment import Segment
from utils import run_gentle
from segmentizer import segmentize
import sys
import json


def align(audio_file_path, text_file_path, anchor_length=40):
    """"
    Align the given audio file and text file with the given starting anchor
    length (N, in Moreno's Algorithm).

    Parameters
    ----------
    audio_file_path : path to the audio file (must be a wav file)
    text_file_path : path to the transcript text file
    anchor_length : number of words needed to define an anchor (default=7)

    Returns
    -------
    result : list of Segment objects
    """

    # load file
    audio_file = AudioSegment.from_file(audio_file_path)

    # load transcript
    with open(text_file_path, "r") as text_file:
        transcript = text_file.read()

    # store audio as a seg and run gentle
    audio_segment = Segment(0, len(audio_file), [], True, audio_file, None)
    gentle_output = run_gentle(audio_segment, transcript)

    # run Moreno's recursive algorithm on initial gentle output
    result = recurse(gentle_output, audio_file, anchor_length=anchor_length)

    ordered_dicts = []
    for seg in result:
        for word in seg.gentle:
            ordered_dicts.append({"word": word.word, "success": word.success(),
                                  "end": word.end, "start": word.start})

    # return result of Moreno's algorithm
    return ordered_dicts


def recurse(gentle_output, audio_file, anchor_length):
    """
    Recursively align the unaligned segments of a given Gentle output.

    Parameters
    ----------
    gentle_output : list of Word objects outputted by previous Gentle run
    audio_file : PyDub object representing the entire audio file
    anchor_length : number of words needed to define an anchor

    Returns
    -------
    res : list of Segment objects
    """
    # convert Gentle output into list of Segment objects
    segs = segmentize(gentle_output, audio_file, anchor_length=anchor_length)

    res = []

    # loop through each segment
    for seg in segs:
        # if aligned --> add to res as is
        if seg.aligned:
            res.append(seg)
        # there is no improvement in alignment --> add unaligned to res as is
        elif len(seg.gentle) == seg.parent_seg_len:
            res.append(seg)
        # if there is no space between anchor points, discard unaligned seg
        elif (seg.end_audio - seg.start_audio) < .001:
            res.append(seg)
        else:
            # else add run recursion through recurse(Gentle(segment))
            res.extend(recurse(run_gentle(seg, seg.get_text()),
                               audio_file, anchor_length=max(anchor_length**.85, 4)))

    return res


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Invalid command line arguments.")
    else:
        output = align(sys.argv[1], sys.argv[2])
        with open(sys.argv[3], "w") as output_file:
            output_file.write(json.dumps(output))
