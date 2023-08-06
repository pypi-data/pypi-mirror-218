import unittest
import os
import argparse
from google.cloud import texttospeech
import wave
from collections import Counter
import uuid

VOICE_CODES = {
    'Female': 'en-US-Wavenet-H',
    'Male': 'en-US-Wavenet-A',
}


class TestSetup(unittest.TestCase):
    def test_setup(self):
        print("starting unittests for speech, checking setup...")

    def test_sst(self):
        ...
        # authenticate with google cloud: https://cloud.google.com/docs/authentication/getting-started
        # from: https://codelabs.developers.google.com/codelabs/cloud-text-speech-python3#0

        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "c:\\Users\\matey\\RFI-Dialog-3134eab04ee8.json"

    def test_concat_wav(self):

        wavs = ['A.wav', 'B.wav']

        concat_wavs(wavs, 'concated_wavs.wav', silence_wav='Silent_2.wav')


def list_languages():
    client = texttospeech.TextToSpeechClient()
    voices = client.list_voices().voices
    languages = unique_languages_from_voices(voices)

    print(f" Languages: {len(languages)} ".center(60, "-"))
    for i, language in enumerate(sorted(languages)):
        print(f"{language:>10}", end="" if i % 5 < 4 else "\n")


def unique_languages_from_voices(voices):
    language_set = set()
    for voice in voices:
        for language_code in voice.language_codes:
            language_set.add(language_code)
    return language_set


def list_voices(language_code=None):
    client = texttospeech.TextToSpeechClient()
    response = client.list_voices(language_code=language_code)
    voices = sorted(response.voices, key=lambda voice: voice.name)

    print(f" Voices: {len(voices)} ".center(60, "-"))
    for voice in voices:
        languages = ", ".join(voice.language_codes)
        name = voice.name
        gender = texttospeech.SsmlVoiceGender(voice.ssml_gender).name
        rate = voice.natural_sample_rate_hertz
        print(f"{languages:<8} | {name:<24} | {gender:<8} | {rate:,} Hz")


def text_to_wav(voice_name, text, filename):
    language_code = "-".join(voice_name.split("-")[:2])
    text_input = texttospeech.SynthesisInput(text=text)
    voice_params = texttospeech.VoiceSelectionParams(
        language_code=language_code, name=voice_name
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16
    )

    client = texttospeech.TextToSpeechClient()
    response = client.synthesize_speech(
        input=text_input, voice=voice_params, audio_config=audio_config
    )

    with open(filename, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to "{filename}"')


def concat_wavs(infiles, outfile, silence_wav=None):

    data = []
    for infile in infiles:
        w = wave.open(infile, 'rb')
        data.append([w.getparams(), w.readframes(w.getnframes())])
        w.close()

        if silence_wav is not None:
            # add silence
            # print('adding silence')
            w2 = wave.open(silence_wav, 'rb')
            data.append([w2.getparams(), w2.readframes(w2.getnframes())])
            w2.close()

    output = wave.open(outfile, 'wb')
    output.setparams(data[0][0])
    for i in range(len(data)):
        output.writeframes(data[i][1])
    output.close()


PAGE_CHARACTER_WIDTH = 120

SCENE_MARKERS = [
    'INT',
    'EXT',
    'EST',
    'INT./EXT',
    'INT/EXT',
    'I/E',
    '.'
]

TRANSITION_MARKERS = [
    'CUT TO:',
    '>',
    'BEGIN',
    'END'
]

IN_SCENE = False
SCENE_ENDING = False
CURRENT_SCENE_NAME = ''
IN_CHARACTER = False
CURRENT_CHARACTER_NAME = ''
SIMULTANEOUS_DIALOGUE = False

_character_line_index = 0
_simultaneous_dialogue_entries = []
word_count_by_character = {}


class SimultaneousDialogEntry(object):

    def __init__(self, character_name, voice_code, line_text, line_filename):
        self.character_name = character_name
        self.voice_code = voice_code
        self.line_text = line_text
        self.line_filename = line_filename


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument("--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("--texttowav", help="run text to wav", action="store_true")
    parser.add_argument("--inputfile", help="input fountain file")

    ARGS = parser.parse_args()

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "c:\\Users\\matey\\RFI-Dialog-3134eab04ee8.json"

    # print(os.environ)

    # list_languages()
    # list_voices("en")

    with open(ARGS.inputfile, 'r') as script_file:
        for line in script_file:
            line = line.strip()
            if line:

                if SCENE_ENDING:
                    IN_SCENE = False
                    _character_line_index = 0

                if line.startswith(tuple(TRANSITION_MARKERS)):

                    # transition
                    offset = ' ' * (PAGE_CHARACTER_WIDTH - len(line))
                    IN_CHARACTER = False
                    IN_SCENE = False
                    print(f'Transition line: {line}')
                    continue

                if line.startswith(tuple(SCENE_MARKERS)):
                    # starting a scene
                    # print(f'Starting Scene line: {line}')
                    IN_SCENE = True
                    IN_CHARACTER = False
                    SCENE_ENDING = False
                    _character_line_index = 0

                    if line.endswith('^'):
                        print(f'Line ends with ^ for SIMULTANEOUS_DIALOGUE')
                        SIMULTANEOUS_DIALOGUE = True

                    CURRENT_SCENE_NAME = line.strip()
                    print(line)
                    continue

                # character names are always in uppercase
                if line.isupper() and IN_SCENE:
                    IN_CHARACTER = True

                    # if marked as ending of scene dialog
                    # that should be concatenated into a single wave
                    # set SCENE_ENDING, to check when
                    # parsing for dialog in IN_CHARACTER
                    if line.endswith('!'):
                        SCENE_ENDING = True

                    # ignore (V.O), (CONT'D), etc..
                    if '(' in line:
                        line = line.split('(')[0].strip()

                    # remove simultaneous marker
                    CURRENT_CHARACTER_NAME = line.replace('^', '').replace('!', '').strip()

                    # print(f'Adding character to word count collection: {line}')
                    word_count_by_character.setdefault(CURRENT_CHARACTER_NAME, Counter())

                    print('\t\t' + CURRENT_CHARACTER_NAME)
                    continue

                if IN_CHARACTER:

                    if SCENE_ENDING:
                        IN_CHARACTER = False

                    # dialog
                    line = line.strip()

                    line_name = CURRENT_SCENE_NAME\
                        .replace('-', ' ')\
                        .replace(' ', '_')\
                        .replace('/', '-')\
                        .replace(':', '-')\
                        .replace('.', '_')\
                        .replace('*', '')

                    line.strip()

                    print(line)

                    # ignore parenthetical
                    if not line.startswith('(') and not line.endswith(')'):

                        line_name = f'{line_name}_{CURRENT_CHARACTER_NAME}_{_character_line_index}'
                        _character_line_index += 1

                        word_count_by_character[CURRENT_CHARACTER_NAME].update(line.split())

                        if not SIMULTANEOUS_DIALOGUE:
                            if CURRENT_CHARACTER_NAME in VOICE_CODES:
                                line_name += '.wav'

                                print(
                                    f'\n************************\nGenerating Dialogue entry for {CURRENT_CHARACTER_NAME} \n\n{line} \n\n{line_name}\n\n********\n')
                                if ARGS.texttowav:
                                    text_to_wav(VOICE_CODES[CURRENT_CHARACTER_NAME], line, line_name)
                            else:
                                print(f'----------------------------0NOT IN VOICE CODES! {CURRENT_CHARACTER_NAME}')
                        else:
                            line_name += f"_{len(_simultaneous_dialogue_entries)}.wav"
                            # print(f'Adding SimultaneousDialogEntry for {CURRENT_CHARACTER_NAME} : {line} : {line_name}')
                            if CURRENT_CHARACTER_NAME in VOICE_CODES:
                                _simultaneous_dialogue_entries.append(SimultaneousDialogEntry(
                                    CURRENT_CHARACTER_NAME, VOICE_CODES[CURRENT_CHARACTER_NAME], line, line_name))

                if not IN_SCENE and not IN_CHARACTER and SCENE_ENDING:

                    if len(_simultaneous_dialogue_entries) > 0:
                        for sde in _simultaneous_dialogue_entries:
                            if sde.character_name in VOICE_CODES:
                                print(f'Generating SimultaneousDialogEntry for {sde.character_name} : {sde.line_text} : {sde.line_filename}')
                                if ARGS.texttowav:
                                    text_to_wav(sde.voice_code, sde.line_text, sde.line_filename)

                        outfile = sde.line_filename.split('_^_')[0] + '.wav'

                        print(f'Scene Name: {CURRENT_SCENE_NAME}: ------------------- CONCAT WAV {sde.line_filename}')

                        if ARGS.texttowav:
                            print('Concating wavs')
                            concat_wavs(
                                [sde.line_filename for sde in _simultaneous_dialogue_entries],
                                        outfile, silence_wav='Silent_2.wav')

                            for sde in _simultaneous_dialogue_entries:
                                os.remove(sde.line_filename)

                        _simultaneous_dialogue_entries.clear()

                        SCENE_ENDING = False
                        SIMULTANEOUS_DIALOGUE = False

    # print out word count by character
    if word_count_by_character:
        for k, v in word_count_by_character.items():
            print(f'{k} word count: {sum(v.values())}')




if __name__ == '__main__':
	unittest.main()
