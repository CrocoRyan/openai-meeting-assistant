from flask import current_app, Response
from flask import jsonify, Blueprint
from flask import request

from utils.constants import FileType
from utils.messsage_utils import get_message_type

bp = Blueprint('main', __name__)


@bp.route('/welcome')
def welcome():
    return "<h1>Welcome!</h1>"


@bp.route('/health', methods=['GET'])
def health_check():
    # health check
    return jsonify(status="healthy", message="Service is up and running"), 200


@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        msg = request.get_json()
        print(msg)

        message_type = get_message_type(msg)
        try:
            if message_type == FileType.TEXT:
                chat_id, txt, time_stamp = current_app.bot_manager.tel_parse_message(msg)
                if current_app.message_handler.is_gpt_entrance(txt):
                    # change to the thread id user select
                    thread_id = txt[1:]
                    current_app.message_handler.set_thread_by_id(chat_id, thread_id)
                    current_app.bot_manager.tel_send_message(chat_id,
                                                             'Chat thread successfully changed to selected meeting!')
                elif current_app.message_handler.is_command(txt):
                    result = current_app.message_handler.execute_command(txt, chat_id)
                    if result is not None:
                        current_app.bot_manager.tel_send_message(chat_id, result)
                else:
                    # chat with gpt assistant
                    current_thread = current_app.message_handler.get_thread_by_id(chat_id)
                    if current_thread is None:
                        # start a new thread
                        current_thread = current_app.ai_agent.create_thread(chat_id, time_stamp)
                        current_app.message_handler.set_thread_by_id(chat_id, current_thread)

                    current_app.ai_agent.respond(chat_id, current_thread, txt)




            else:
                chat_id, file_id, file_type = current_app.bot_manager.tel_parse_non_text_message(msg)

                file_path = current_app.bot_manager.tel_upload_file(file_id)
                if file_path is not None:
                    current_app.bot_manager.tel_send_message(chat_id, "upload success")
                    if file_type != FileType.AUDIO:
                        current_app.bot_manager.tel_send_message(chat_id,
                                                                 "However, the bot doesn't support this type of file "
                                                                 "at the moment")
                    else:
                        current_app.message_handler.add_audio_to_chat_state(chat_id, file_path)
                        current_app.bot_manager.tel_send_language_option(chat_id)

                else:
                    current_app.bot_manager.tel_send_message(chat_id,
                                                             "upload failed, file size may exceeds the limit of bot capability(20MB)")
        except Exception as e:
            print(f"An Exception occurred: {e}")
        return Response('ok', status=200)

    else:
        return "<h1>Incorrect invocation</h1>"
