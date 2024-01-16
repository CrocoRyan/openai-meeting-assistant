class ChatState:
    def __init__(self, thread_id=None, audio_cache_path=None, language_code=None, audio_transcript=None):
        self.thread_id = thread_id
        self.audio_cache_path = audio_cache_path
        self.language_code = language_code
        self.transcript = audio_transcript
