import json
import os

import requests

from app.models.ChatState import ChatState
from flask import current_app

class MessageHandler:
    def __init__(self,token):
        self.user_thread_state={6276730573:ChatState()}
        self.bot_token=token

        with open(os.path.join(os.getcwd(),'commands.json'), 'r') as file:
            self.commands = json.load(file)
        self.update_command()

    def update_command(self):
        data = json.dumps({'commands': self.commands})
        URL = f"https://api.telegram.org/bot{self.bot_token}/setMyCommands"
        headers = {'Content-Type': 'application/json'}
        response = requests.post(URL, headers=headers, data=data)
        if response.status_code == 200:
            print("update command success")
        else:
            print("update command failed")
    def is_command(self,message:str):
        if message.startswith('/'):
            if hasattr(self, message[1:]):
                return True
            else:
                return False
    def get_thread_by_id(self, chat_id):
        return self.user_thread_state[chat_id].thread_id
    def set_thread_by_id(self, chat_id, thread_id):
        self.user_thread_state[chat_id].thread_id=thread_id
    def is_gpt_entrance(self,message:str):
        if message.startswith('*'):
            result=current_app.db_manager.get_doc_by_thread(message[1:])
            if result is None:
                return False
            else: return True
        else: return False

    def execute_command(self, message:str, chat_id:str):
        command=message[1:]
        if hasattr(self, command):
            method = getattr(self, command)
            return method(chat_id)
        else:
            return "Command not recognized."

    def start(self,chat_id):
        self.user_thread_state[chat_id]=ChatState()

        content_lines=["Hi! Welcome to the meeting assistant bot! I'm here to help you with meeting summaries. Just provide me with the meeting audio, and I'll get started on transcripting & creating the summary for you. Below are some commands you can use:"]
        for command in self.commands:
            content_lines.append(command['command']+' - '+command['description'])

        # find all gpt conversation history for a user
        return '\n'.join(content_lines)
    def add_audio_to_chat_state(self, chat_id, file_path):
        self.user_thread_state[chat_id].audio_cache_path=file_path
    def add_thread_to_chat_state(self, chat_id, thread_id):
        self.user_thread_state[chat_id].thread_id=thread_id
    def set_English(self, chat_id):
        self.user_thread_state[chat_id].language_code="en-US"
        current_app.bot_manager.tel_send_message(chat_id,"audio language support set to English, start processing...")
        self.transcript(chat_id)
        return "Speech recognized"
    def set_Chinese(self, chat_id):
        self.user_thread_state[chat_id].language_code="zh-CN"
        current_app.bot_manager.tel_send_message(chat_id,"audio language support set to Chinese, start processing...")
        self.transcript(chat_id)
        return "Speech recognized"
    def transcript(self,chat_id):
        audio_path=self.user_thread_state[chat_id].audio_cache_path
        language_code=self.user_thread_state[chat_id].language_code
        self.user_thread_state[chat_id].transcript=current_app.speech_service.recognize_speech_from_file(audio_path, language_code)
        current_app.ai_agent.respond(chat_id, self.user_thread_state[chat_id].thread_id, self.user_thread_state[chat_id].transcript+'\n Please summarize the speech')


    def pull_up_history(self,chat_id):
        # find all gpt conversation history for a user
        raw_results = current_app.db_manager.get_user_snapshots(chat_id)
        if raw_results is None:
            return "No meetings history can be found"
        # Iterate through the results and print them
        description=[]
        mapping=[]
        for document in raw_results:
            description.append(f"Meeting[{document['innerIndex']}]: "+f"CreatedTime: {document['createdTime']}")
            mapping.append({"text":document['innerIndex'],"callback_data":"*"+document['threadID']})

        current_app.bot_manager.tel_send_gpt_entrance(chat_id,'\n'.join(description),mapping)
        return "Please select on the pop up above"
        # return result
    # def jump_into_meeting(self,index_id):
    #     # update thread_state, ai assistant ready