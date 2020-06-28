import glob
import logging
import os
import sys

from pydub import AudioSegment
from pydub import silence

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)-8s %(message)s')
logger = logging.getLogger()


def get_all_audio_files(directory):
    """
    Function that returns list of audio files from the directory 'audios'.
    :param directory:
    :return: list of files
    """

    types = ('*.mp3', '*.wav')
    files_grabbed = []
    for files in types:
        files_grabbed.extend(glob.glob('{}/{}'.format(directory, files)))
    return sorted(files_grabbed)


def split(audio_files, audio_path):
    """
    Function that split an audio file only on a silence position if possible.
    Please change the parameters
        - audio_max_length
        - min_silence
        - silence_threshold
    for your use case.
    Therefore please take a look into the official repo of pydub silence:
    https://github.com/jiaaro/pydub/blob/master/pydub/silence.py

    :param audio_files:
    :param audio_path:
    :return:
    """

    output_path = 'splitted'

    if not os.path.exists(output_path):
        os.mkdir(output_path)

    # Max length (59 seconds)
    audio_max_length = 59000

    # Parameters for silence detection
    min_silence = 100
    silence_threshold = -40

    for audio in audio_files:
        filename = audio.split('/')[-1]
        filename_without_ext = filename.split('.')[0]  # Get filename without extension
        os.makedirs(os.path.dirname('{0}/{1}/'.format(output_path, filename_without_ext)), exist_ok=True)

        if filename.endswith('.mp3'):
            audio_format = 'mp3'
            audio_segment = AudioSegment.from_mp3('{}/{}'.format(audio_path, filename))
        elif filename.endswith('.wav'):
            audio_format = 'wav'
            audio_segment = AudioSegment.from_wav('{}/{}'.format(audio_path, filename))
        else:
            logger.error('Audio files have a file format that is not supported.')
            sys.exit()

        # Silence detection
        chunks = silence.detect_silence(audio_segment, min_silence_len=min_silence, silence_thresh=silence_threshold)

        start = 0
        part = 0
        ends = []

        for _, y in chunks:
            ends.append(y)

        if len(audio_segment) < audio_max_length:
            audio_segment.export('{}/{}/{}'.format(output_path, filename_without_ext,
                                                   '{}_{}.{}'.format(filename_without_ext, part, audio_format)),
                                 format=audio_format)
            logger.info('Export File: {}'.format('{}_{}.{}'.format(filename_without_ext, part, audio_format)))
        else:
            while start < ends[-1]:
                current_end = [i for i in ends if i <= start + audio_max_length][-1]
                # If there is no possibility to cut on an end that is in ends list (current_end - start == 0)
                # make a hard cut
                if (current_end - start) <= 0:
                    current_end = start + audio_max_length
                    logger.warning('Hard cut')
                audio_segment[start:current_end].export(
                    '{}/{}/{}'.format(output_path, filename_without_ext,
                                      '{}_{}.{}'.format(filename_without_ext, part, audio_format)),
                    format=audio_format)
                start = current_end
                part += 1
                logger.info('Export File: {}'.format('{}_{}.{}'.format(filename_without_ext, part, audio_format)))


if __name__ == '__main__':
    """
    Entrypoint of the application.
    """

    input_path = 'audios'

    if not os.path.exists(input_path):
        logger.error('The directory "audios/" does not contain any audio files.')
        sys.exit()

    audios = get_all_audio_files(input_path)
    split(audios, input_path)
