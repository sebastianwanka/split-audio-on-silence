# Split audio on silence
This application cuts audio files into small pieces with a defined maximum length. 
It is taken care that the audio file is only cut at the places where silence 
is present. This is very important, for example, if you want to cut recorded 
dictations not in the middle of a spoken word. The maximum length of a cut 
audio file as well as the parameters to define silence have to be adapted 
to the respective use case. 

The default values are currently set to:


`audio_max_length = 59000` (ms)

`min_silence = 100` (ms)

`silence_threshold = -40` (dB)

The tool `pydub` is used to detect silence:
https://github.com/jiaaro/pydub

## Local Setup
For developing in Python it is recommended to use a virtual environment tool like 
conda: https://docs.conda.io/en/latest/miniconda.html 

To install packages just execute 

```pip install -r requirements.txt```

Furthermore you have to make sure that `ffmpeg` is installed on your machine:
https://ffmpeg.org/

## Use
- Please move the audio files you want to split in the directory `audios`.
- Execute `.main.py`

## Supported file formats
Only the file formats `.mp3` and `.wav` are supported.