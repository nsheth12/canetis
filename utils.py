import os
from segment import Segment
from pydub import AudioSegment
import sys
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


def fix_unaligned (gentle_output, audio_file_length):
	"""
	Give approximate start/end times to unaligned words in the Gentle output.

	Parameters
	----------
	gentle_output : list of Word objects returned by Gentle
	audio_file : AudioSegment object representing the entire audio file
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
