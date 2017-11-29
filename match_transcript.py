import os, re

kelly_path = "../kelly_qtype_csvs/"
audio_path = "../mono8khz/"


kelly_names = os.listdir(kelly_path)
kelly_ids = [re.split("_|-", f)[0] for f in kelly_names]

audio_names = os.listdir(audio_path)
audio_ids = [re.split("_|-", f)[0] for f in audio_names]

result = {}

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

clean_audio(audio_names, audio_ids)					

for audio_index, audio_id in enumerate(audio_ids):
	try:
		pos = kelly_ids.index(audio_id)
		result[audio_names[audio_index]] = kelly_names[pos]
	except:
		print("No transcript for ", audio_id)

print(len(result))















