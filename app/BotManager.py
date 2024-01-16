import json
from enum import Enum

import requests

from utils.constants import FileType

from utils.file_utils import create_folder_if_not_exist
from utils.messsage_utils import is_callback, get_message_type


class BotManager:
    def __init__(self,token):
        self.bot_token=token

    def tel_parse_message(self, message):
        if is_callback(message):
            chat_id = message['callback_query']['from']['id']
            txt = message['callback_query']['data']
            time_stamp = message['callback_query']['message']['date']
        else:
            chat_id = message['message']['chat']['id']
            txt = message['message']['text']
            time_stamp = message['message']['date']

        print("chat_id-->", chat_id)
        print("txt-->", txt)
        print("time-->", time_stamp)

        return chat_id, txt, time_stamp

    def tel_send_message(self,chat_id, text):
        url = f'https://api.telegram.org/bot{self.bot_token}/sendMessage'
        payload = {
            'chat_id': chat_id,
            'text': text
        }

        r = requests.post(url, json=payload)
        return r

    def tel_send_messages(self,chat_id, text_list):
        for text in text_list:
            self.tel_send_message(chat_id,text)

    def tel_parse_non_text_message(self, message):
        print("message-->", message)

        chat_id = message['message']['chat']['id']
        message_type = get_message_type(message)

        if message_type == FileType.PHOTO:
            file_id = message['message']['photo'][0]['file_id']
        elif message_type == FileType.VIDEO:
            file_id = message['message']['video']['file_id']
        elif message_type == FileType.AUDIO:
            file_id = message['message']['audio']['file_id']
        elif message_type == FileType.OTHERS:
            file_id = message['message']['document']['file_id']
        else:
            print("NO file found-->>")

        print(f"g_chat_id-->{chat_id}")
        print(f"g_{message_type}_id-->{file_id}")

        return chat_id, file_id, message_type

    # def tel_parse_get_message(self,message):
    #     print("message-->", message)
    #
    #     try:
    #         g_chat_id = message['message']['chat']['id']
    #         g_file_id = message['message']['photo'][0]['file_id']
    #         print("g_chat_id-->", g_chat_id)
    #         print("g_image_id-->", g_file_id)
    #
    #         return g_chat_id,g_file_id, FileType.PHOTO
    #     except:
    #         try:
    #             g_chat_id = message['message']['chat']['id']
    #             g_file_id = message['message']['video']['file_id']
    #             print("g_chat_id-->", g_chat_id)
    #             print("g_video_id-->", g_file_id)
    #
    #             return g_chat_id,g_file_id, FileType.VIDEO
    #         except:
    #             try:
    #                 g_chat_id = message['message']['chat']['id']
    #                 g_file_id = message['message']['audio']['file_id']
    #                 print("g_chat_id-->", g_chat_id)
    #                 print("g_audio_id-->", g_file_id)
    #
    #                 return g_chat_id,g_file_id, FileType.AUDIO
    #             except:
    #                 try:
    #                     g_chat_id = message['message']['chat']['id']
    #                     g_file_id = message['message']['document']['file_id']
    #                     print("g_chat_id-->", g_chat_id)
    #                     print("g_file_id-->", g_file_id)
    #
    #                     return g_chat_id,g_file_id, FileType.OTHERS
    #                 except:
    #                     print("NO file found found-->>")


    def tel_upload_file(self,file_id):
        url = f'https://api.telegram.org/bot{self.bot_token}/getFile?file_id={file_id}'
        a = requests.post(url)
        json_resp = json.loads(a.content)
        print("a-->", a)
        print("json_resp-->", json_resp)

        # Check if the request was successful
        if a.status_code != 200 or 'result' not in json_resp:
            print("Error fetching file from Telegram.")
            return None

        file_path = json_resp['result']['file_path']
        print("file_path-->", file_path)

        url_1 = f'https://api.telegram.org/file/bot{self.bot_token}/{file_path}'
        b = requests.get(url_1)
        file_content = b.content

        try:
            create_folder_if_not_exist(file_path)
            with open(file_path, "wb") as f:
                f.write(file_content)
        except FileNotFoundError:
            print("The specified file path does not exist.")
            return None
        except PermissionError:
            print("Insufficient permission to write to the file.")
            return None
        except OSError as e:
            print(f"An error occurred while writing to the file: {e}")
            return None

        return file_path


    def tel_send_language_option(self,chat_id):
        url = f'https://api.telegram.org/bot{self.bot_token}/sendMessage'

        payload = {
            'chat_id': chat_id,
            'text': "Please select the language of this audio:",
            'reply_markup': {
                "inline_keyboard": [[
                    {
                        "text": "English",
                        "callback_data": "/set_English"
                    },
                    {
                        "text": "中文",
                        "callback_data": "/set_Chinese"
                    }]
                ]
            }
        }
        r = requests.post(url, json=payload)
        return r
    def tel_send_gpt_entrance(self,chat_id,reply,mapping):
        url = f'https://api.telegram.org/bot{self.bot_token}/sendMessage'

        payload = {
            'chat_id': chat_id,
            'text': f"{reply}",
            'reply_markup': {
                "inline_keyboard": [mapping]
            }
        }
        r = requests.post(url, json=payload)
        return r
