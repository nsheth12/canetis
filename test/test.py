import gentle
import os
import json
from align import align

DIR_PATH = os.path.dirname(os.path.abspath(__file__))


def test_gentle(audio_path, transcript_path, transcript_name):
    # get transcript text
    transcript_text = ""
    with open(transcript_path) as f:
        transcript_text = f.read()

    # run Gentle
    print "Running Gentle on", transcript_name
    resources = gentle.Resources()
    with gentle.resampled(audio_path) as wavfile:
        aligner = gentle.ForcedAligner(resources, transcript_text)
        result = aligner.transcribe(wavfile).words

    # create gentle_results directory if it doesn't already exist
    # usually better to use try-catch here, but not worried about race conditions right now
    if not os.path.exists(os.path.join(DIR_PATH, "gentle_results")):
        os.makedirs(os.path.join(DIR_PATH, "gentle_results"))

    # write Gentle output to gentle_results directory
    with open(os.path.join(DIR_PATH, "gentle_results", transcript_name + ".txt"), "w") as f:
        output = []
        for word in result:
            output.append({"word": word.word, "success": word.success(),
                           "end": word.end, "start": word.start})
        json.dump(output, f)

    successful_words_gentle = 0
    total_words_gentle = 0

    with open(os.path.join(DIR_PATH, "gentle_results", transcript_name + ".txt")) as gentle_file:
        gentle_output = json.load(gentle_file)

        for word in gentle_output:
            if word["success"]:
                successful_words_gentle += 1
            total_words_gentle += 1

    print "Gentle successful:", successful_words_gentle
    print "Gentle total:", total_words_gentle
    print


def test_canetis(audio_path, transcript_path, transcript_name):
    # run Canetis
    print "Running Canetis on", transcript_name
    canetis_output = align(audio_path, transcript_path)

    # create canetis_results directory if it doesn't already exist
    if not os.path.exists(os.path.join(DIR_PATH, "canetis_results")):
        os.makedirs(os.path.join(DIR_PATH, "canetis_results"))

    # write Canetis output to canetis_results directory
    with open(os.path.join(DIR_PATH, "canetis_results", transcript_name + ".txt"), "w") as f:
        json.dump(canetis_output, f)

    successful_words_canetis = 0
    total_words_canetis = 0

    with open(os.path.join(DIR_PATH, "canetis_results", transcript_name + ".txt")) as canetis_file:
        canetis_output = json.load(canetis_file)

        for word in canetis_output:
            if word["success"]:
                successful_words_canetis += 1
            total_words_canetis += 1

    print "Canetis successful:", successful_words_canetis
    print "Canetis total:", total_words_canetis
    print


for audio_name in os.listdir(os.path.join(DIR_PATH, "audio")):
    transcript_name = os.path.splitext(audio_name)[0] + ".trn"

    audio_path = os.path.join(DIR_PATH, "audio", audio_name)
    transcript_path = os.path.join(DIR_PATH, "transcripts", transcript_name)

    if not os.path.isfile(transcript_path):
        continue

    if "MODE" not in os.environ:
        test_gentle(audio_path, transcript_path, transcript_name)
        test_canetis(audio_path, transcript_path, transcript_name)
    elif os.environ["MODE"] == "gentle":
        test_gentle(audio_path, transcript_path, transcript_name)
    else:
        test_canetis(audio_path, transcript_path, transcript_name)
