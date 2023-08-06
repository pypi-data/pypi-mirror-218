from datetime import datetime, timedelta
from queue import Queue
from tempfile import NamedTemporaryFile
from time import sleep
from sys import platform
import numpy as np
import soundfile as sf
import torch
import whisper
from whisper.utils import *
from prompt4all_liteon import context

cxt=context._context()


__all__ = ["whisper_model","to_formated_time","recognize_whisper","record_timeout","phrase_timeout","no_speech_threshold","load_whisper_model"]

whisper_model=None
record_timeout=2
phrase_timeout=3
no_speech_threshold=0.6

def load_whisper_model():
    if cxt.whisper_model is None:
        cxt.whisper_model = whisper.load_model('medium', device='cpu')
        print('Whisper small model載入完成!')
    return cxt.whisper_model

def to_formated_time(float_time):
    return format_timestamp(float_time,always_include_hours=True)

def recognize_whisper(audio_data,word_timestamps=False,language='zh', translate=False, **transcribe_options):
    """
    Performs speech recognition on ``audio_data`` (an ``AudioData`` instance), using Whisper.

    The recognition language is determined by ``language``, an uncapitalized full language name like "english" or "chinese". See the full language list at https://github.com/openai/whisper/blob/main/whisper/tokenizer.py

    model can be any of tiny, base, small, medium, large, tiny.en, base.en, small.en, medium.en. See https://github.com/openai/whisper for more details.

    If show_dict is true, returns the full dict response from Whisper, including the detected language. Otherwise returns only the transcription.

    You can translate the result to english with Whisper by passing translate=True

    Other values are passed directly to whisper. See https://github.com/openai/whisper/blob/main/whisper/transcribe.py for all options
    """

    if cxt.whisper_model is None:
        cxt.whisper_model=whisper.load_model('small', device='cuda')
        return {"text":'Whisper medium model載入完成!',"no_speech_prob":0.001}

    # 16 kHz https://github.com/openai/whisper/blob/28769fcfe50755a817ab922a7bc83483159600a9/whisper/audio.py#L98-L99
    if not isinstance(audio_data,np.ndarray):
        # wav_bytes = audio_data.get_wav_data(convert_rate=16000)
        # wav_stream = io.BytesIO(wav_bytes)
        # audio_array, sampling_rate = sf.read(wav_stream)
        # audio_array = audio_array.astype(np.float32)
        result = cxt.whisper_model.transcribe(
            audio_data,
            language=language,
            word_timestamps=word_timestamps,
            verbose=True,
            task="translate" if translate else None,
            fp16=True if cxt.whisper_model.device=="cuda" and torch.cuda.is_available() else False,
            no_speech_threshold=0.65,
            initial_prompt="#zh-tw 使用ChatGPT以及Whisper會議記錄逐字稿",
            **transcribe_options
        )
    else:
        audio_array=audio_data.astype(np.float32)
        result = cxt.whisper_model.transcribe(
            audio_array,
            language=language,
            word_timestamps=word_timestamps,
            task="translate" if translate else None,
            fp16=True if cxt.whisper_model.device=="cuda" and torch.cuda.is_available() else False,
            no_speech_threshold=0.6,
            initial_prompt="#zh-tw 使用ChatGPT以及Whisper會議記錄逐字稿",
            **transcribe_options
        )

    return result



