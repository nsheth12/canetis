import os, re


#get id from a given filename
def get_id(name):
	return re.split("_|-", name)[0]

#generate id list that corresponds to audio_names
def get_ids(names):
	ids = []	
	for name in names:
		ids.append(get_id(name))
	
	return ids		


def remove_duplicates(audio_names, audio_ids):
	i = 0
	while i < len(audio_ids) - 1:
		length = len(audio_ids)
		
		try:
			#delete all duplicates
			while audio_ids[i] == audio_ids[i+1]:
				del audio_names[i+1]
				del audio_ids[i+1]

			#if anything was deleted, delete current position
			if length != len(audio_ids):
				del audio_ids[i]
				del audio_names[i]
			else:
				i += 1
		except:
			pass

	
# Cleans the audio files of duplicates and
# returns corresponding audio_ids list

def load_data(dir_path, audio=False):
	
	names = os.listdir(dir_path)

	names.sort()

	ids = get_ids(names)

	
	if audio:
		remove_duplicates(names, ids)
	


	return names, ids
	
	

kelly_path = "../kelly_qtype_csvs/"
backup_path = "../csv_forensic_interview_transcipts/"
audio_path = "../mono8khz/"

"""
The folders within the forensic_interview_transcripts directory
did not have any files that were not already in the forensic_interview_transcripts
directory, so we removed them from the search path
"""

kelly_names, kelly_ids = load_data(kelly_path)

backup_names, backup_ids = load_data(backup_path)


audio_names, audio_ids = load_data(audio_path, audio=True)


result = {}


for audio_index, audio_id in enumerate(audio_ids):
	#print("Audio ID: ", audio_id, " Audio Name: ", audio_names[audio_index])
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
	

"""
for key, value in result.items():
	print(key, ": ", value)
"""
print(str(len(result)) + " transcripts were matched.")











