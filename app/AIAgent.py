import json
import time
from time import sleep

from flask import current_app
from openai import OpenAI

from utils.messsage_utils import text_progress_bar, split_gpt_text


class AIAgent:
    def __init__(self, assistant_id, api_key):
        self.assistant_id = assistant_id
        self.client = OpenAI(api_key=api_key)

    def parse_json_garbage(self, s):
        # function to truncate garbage part from the response
        s = s[next(idx for idx, c in enumerate(s) if c in "{["):]
        # return s
        try:
            return json.loads(s)
        except json.JSONDecodeError as e:
            return json.loads(s[: e.pos])

    def create_thread(self, user_id, time_stamp=None):

        # create new thread for the user
        thread = self.client.beta.threads.create()
        if time_stamp is None:
            time_stamp = time.time()
        current_app.db_manager.insert_data(user_id, thread.id, time_stamp)
        print(f"User data for UserID '{user_id}' added successfully.")
        return thread.id

    def check_and_add_user_data(self, user_id, inner_index=0):
        # Check if user data exists for the given user_id
        if not current_app.db_manager.check_user_exists(user_id):
            # If user data doesn't exist, insert data for the user
            thread = self.client.beta.threads.create()
            current_app.db_manager.insert_data(user_id, thread.id, self.assistant_id)
            print(f"User data for UserID '{user_id}' added successfully.")

        else:
            print(f"User data for UserID '{user_id}' already exists.")
            # user_data = manager.get_user_data(user_id,inner_index)
            # print(user_data)
            # return user_data
        user_data = current_app.db_manager.get_user_data(user_id, inner_index)
        return user_data

    def respond(self, user_id, thread_id, user_input):
        try:

            if thread_id is None:
                thread_id = current_app.ai_agent.create_thread(user_id)
                current_app.message_handler.set_thread_by_id(user_id, thread_id)

            # add user input to thread
            self.client.beta.threads.messages.create(
                thread_id=thread_id, role="user", content=user_input
            )
            # appending user response in the database
            current_app.db_manager.append_message(user_id, thread_id, user_input, "user")

            # Run the Assistant
            run = self.client.beta.threads.runs.create(
                thread_id=thread_id, assistant_id=self.assistant_id
            )

            # Check if the Run requires action (function call)
            fake_progress = 1
            while True:
                run_status = self.client.beta.threads.runs.retrieve(
                    thread_id=thread_id, run_id=run.id
                )
                print(f"Run status: {run_status.status}")
                current_app.bot_manager.tel_send_message(user_id, text_progress_bar(fake_progress, 10))
                if run_status.status == "completed":
                    break
                fake_progress += 1
                sleep(5)  # Wait for a second before checking again

            # Retrieve and return the latest command from the assistant
            current_app.bot_manager.tel_send_message(user_id, text_progress_bar(10, 10))

            response = self.client.beta.threads.messages.list(thread_id=thread_id).data[0].content[0].text.value
            # json_response = parse_json_garbage(response)
            print(f"Assistant response: {response}")

            # todo: fix json response
            # json_response = self.parse_json_garbage(response)
            # appending assistant response in the database
            current_app.db_manager.append_message(user_id, thread_id, response, "assistant_response")
            splited_messages = split_gpt_text(response)
            for message in splited_messages:
                current_app.bot_manager.tel_send_message(user_id, message)

        # error handling
        except Exception as a:
            a = str(a)
            #  Handle exception
            print(a)
            current_app.bot_manager.tel_send_message(user_id, {
                "success": False,
                "error": {
                    "statusCode": 500,
                    "command": "Something went wrong!",
                    "errorMessage": a,
                },
            })
