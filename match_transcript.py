import os, re

# get the "id" number at the beginning of the filename
def get_ids(names):
	return [re.split("_|-", f)[0] for f in names]

# remove all audio files that have multiple audio files for the same
# transcript
def clean_audio(audio_names, audio_ids):
	audio_names.sort()
	audio_ids.sort()

	i = 0
	while i < len(audio_ids) - 1:
		length = len(audio_ids)
		while audio_ids[i] == audio_ids[i+1]:
			del audio_names[i+1]
			del audio_ids[i+1]
		if length != len(audio_ids):
			del audio_ids[i]
			del audio_names[i]
		else:
			i += 1

kelly_path = "../kelly_qtype_csvs/"
backup_path = "../forensic_interview_transcripts/"
audio_path = "../mono8khz/"

"""
The folders within the forensic_interview_transcripts directory
did not have any files that were not already in the forensic_interview_transcripts
directory, so we removed them from the search path
"""

kelly_names = os.listdir(kelly_path)
kelly_ids = get_ids(kelly_names)

backup_names = os.listdir(backup_path)
backup_ids = get_ids(backup_names)

audio_names = os.listdir(audio_path)
audio_ids = get_ids(audio_names)

result = {}

#clean_audio(audio_names, audio_ids)				

for audio_index, audio_id in enumerate(audio_ids):
	print("Audio ID: ", audio_id, " Audio Name: ", audio_names[audio_index])
	try:
		pos = kelly_ids.index(audio_id)
		result[audio_names[audio_index]] = kelly_names[pos]
		#print("Audio ID: ", audio_id, " Transcript ID: ", kelly_ids[pos])
	except:
		try:
			pos = backup_ids.index(audio_id)
			result[audio_names[audio_index]] = backup_names[pos]
		except:
			pass
			#print("No transcript for " + audio_id)
			
for key, value in result.items():
	print(key, ": ", value)
#print(len(result), "transcripts were matched.")














