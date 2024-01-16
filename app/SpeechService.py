import azure.cognitiveservices.speech as speechsdk

from app.models import AzureAudioStreamCallback
from utils.audio_utils import convert_audio_to_standard_stream


class SpeechService:
    def __init__(self, subscription, region):
        # self.speech_config.speech_recognition_language = language_code
        self.speech_config = speechsdk.SpeechConfig(subscription, region)
        # self.speech_config =current_app.speech_config

    def recognize_speech_from_file(self, filename, language_code="en-US"):
        self.speech_config.speech_recognition_language = language_code
        audio_stream = convert_audio_to_standard_stream(filename)
        wave_format = speechsdk.audio.AudioStreamFormat(samples_per_second=16000, bits_per_sample=16,
                                                        channels=1)
        callback = AzureAudioStreamCallback(audio_stream)
        stream = speechsdk.audio.PullAudioInputStream(callback, wave_format)
        audio_config = speechsdk.audio.AudioConfig(stream=stream)
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config, audio_config=audio_config)
        return self.perform_recognition(speech_recognizer)

    def perform_recognition(self, recognizer):
        print("Starting speech recognition...")
        speech_recognition_result = recognizer.recognize_once_async().get()

        if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
            return "Recognized speech: {}".format(speech_recognition_result.text)
        elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
            return "No speech could be recognized."
        elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_recognition_result.cancellation_details
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                return "Error details: {}".format(cancellation_details.error_details)
            return "Speech Recognition canceled."
        return "Unknown error occurred."

# Example usage
# if __name__ == "__main__":

#     speech_manager = SpeechManager(language="zh-CN")
#     print(speech_manager.recognize_speech_from_file("./speech-to-text-sample-chinese.wav"))

# For recognizing speech from microphone, uncomment the following line:
# print(speech_manager.recognize_speech_from_microphone())
