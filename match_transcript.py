import os, re


def get_ids(names):
	return [re.split("_|-", f)[0] for f in names]

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

def clean_ids(ids):
	ids = ids
	return [ re.sub("\D", "", bad_id) for bad_id in ids ]


kelly_path = "../kelly_qtype_csvs/"
back_up_path = "../forensic_interview_transcripts/"
audio_path = "../mono8khz/"

"""
The folders within the forensic_interview_transcripts directory
did not have any files that were not already in the forensic_interview_transcripts
directory, so we removed them from the search path
"""


kelly_names = os.listdir(kelly_path)
kelly_ids = get_ids(kelly_names)

backup_names = os.listdir(back_up_path)
backup_ids = get_ids(backup_names)
clean_back_up_ids = clean_ids(backup_ids)

print(clean_back_up_ids)

#last_resort_names = os.listdir(last_resort_path)
#last_resort_ids = get_ids(last_resort_names)
##print(len(backup_ids))

audio_names = os.listdir(audio_path)
audio_ids = [re.split("_|-", f)[0] for f in audio_names]

result = {}
	

clean_audio(audio_names, audio_ids)
					

for audio_index, audio_id in enumerate(audio_ids):
	try:
		pos = kelly_ids.index(audio_id)
		result[audio_names[audio_index]] = kelly_names[pos]
	except:
		try:
			pos = backup_ids.index(audio_id)
			result[audio_names[audio_index]] = backup_names[pos]

		except:	
			try:
				pos = clean_back_up_ids.index(audio_id)
			except:
				
				print("No transcript for " + audio_id)
			

print(len(result))















