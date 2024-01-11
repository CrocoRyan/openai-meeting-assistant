import ffmpeg
import io
import os
import azure.cognitiveservices.speech as speechsdk

from app.models.AzureAudioStreamCallback import AzureAudioStreamCallback


# Convert audio file to WAV format and return as a stream
def convert_audio_to_standard_stream(input_path):
    out, _ = (
        ffmpeg
        .input(input_path)
        .output('pipe:', format='wav', acodec='pcm_s16le', ac=1, ar='16k')
        .run(capture_stdout=True, capture_stderr=True)
    )
    return io.BytesIO(out)



# # Example usage
# speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
# speech_config.speech_recognition_language="zh-CN"
# wave_format = speechsdk.audio.AudioStreamFormat(samples_per_second=16000, bits_per_sample=16,
#                                                 channels=1)
# audio_stream = convert_audio_to_standard_stream('speech-to-text-sample-english.m4a')
# callback = AzureAudioStreamCallback(audio_stream)
# stream = speechsdk.audio.PullAudioInputStream(callback, wave_format)
# audio_config = speechsdk.audio.AudioConfig(stream=stream)
# speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
#
# speech_recognition_result = speech_recognizer.recognize_once_async().get()
#
# if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
#     print("Recognized: {}".format(speech_recognition_result.text))
# elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
#     print("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))
# elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
#     cancellation_details = speech_recognition_result.cancellation_details
#     print("Speech Recognition canceled: {}".format(cancellation_details.reason))
#     if cancellation_details.reason == speechsdk.CancellationReason.Error:
#         print("Error details: {}".format(cancellation_details.error_details))
#         print("Did you set the speech resource key and region values?")