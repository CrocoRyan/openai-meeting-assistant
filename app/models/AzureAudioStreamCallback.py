from azure.cognitiveservices.speech import audio


# Audio stream callback class for Azure Speech SDK
class AzureAudioStreamCallback(audio.PullAudioInputStreamCallback):
    def __init__(self, stream):
        super().__init__()
        self._stream = stream

    def read(self, buffer):
        data = self._stream.read(len(buffer))
        buffer[:len(data)] = data
        return len(data)

    def close(self):
        self._stream.close()

