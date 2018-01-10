from align import align


# Set up test
text_file_path = "/home/coder/Desktop/alignment_nihar_kian/kelly_qtype_cleaned/2-Adrian-5-Transcript.txt"
audio_file_path = "/home/coder/Desktop/alignment_nihar_kian/mono8khz/2_16000.wav"

result = align(audio_file_path, text_file_path)


alignedCount = 0
totalCount = 0
for seg in result:
	words = seg.gentle
	for word in words:
		#print(word.word, word.start, word.end, word.success())
		if word.success():
			alignedCount += 1
		totalCount += 1

print("Moreno words aligned: ", alignedCount)
print("Total count: ", totalCount)