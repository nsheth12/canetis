import gentle
from align import align
import os
import json


def process_file(basename):
    successful_words_canetis = 0
    total_words_canetis = 0
    successful_words_gentle = 0
    total_words_gentle = 0

    # canetis part
    with open(os.path.join("canetis_results", basename)) as canetis_file:
        canetis_output = json.load(canetis_file)

        for word in canetis_output:
            if word["success"]:
                successful_words_canetis += 1
            total_words_canetis += 1

    # gentle part
    with open(os.path.join("gentle_results", basename)) as gentle_file:
        gentle_output = json.load(gentle_file)

        for word in gentle_output:
            if word["success"]:
                successful_words_gentle += 1
            total_words_gentle += 1
        # successful_words_gentle = int(gentle_file.readline().strip())
        # total_words_gentle = int(gentle_file.readline().strip())

    print "Gentle successful:", successful_words_gentle
    print "Canetis successful:", successful_words_canetis
    print "Gentle total:", total_words_gentle
    print "Canetis total:", total_words_canetis
    print


for audio_name in os.listdir("audio"):
    transcript_name = os.path.splitext(audio_name)[0] + ".trn"

    audio_path = os.path.join("audio", audio_name)
    transcript_path = os.path.join("transcripts", transcript_name)

    if not os.path.isfile(transcript_path):
        continue

    # get transcript text
    transcript_text = ""
    with open(transcript_path) as f:
        transcript_text = f.read()

    # run Gentle
    print("About to run Gentle on " + transcript_name)
    resources = gentle.Resources()
    with gentle.resampled(audio_path) as wavfile:
        aligner = gentle.ForcedAligner(resources, transcript_text)
        result = aligner.transcribe(wavfile).words

    with open(os.path.join("gentle_results", transcript_name + ".txt"), "w") as f:
        output = []
        for word in result:
            output.append({"word": word.word, "success": word.success(),
                           "end": word.end, "start": word.start})
        json.dump(output, f)

    # run Canetis
    print("About to run Canetis on " + transcript_name)
    canetis_output = align(audio_path, transcript_path)

    with open(os.path.join("canetis_results", transcript_name + ".txt"), "w") as f:
        json.dump(canetis_output, f)

    process_file(transcript_name + ".txt")
