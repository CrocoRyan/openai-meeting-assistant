from flask import current_app
from flask import jsonify, Blueprint

from flask import request
from flask import Response

from utils.constants import FileType

bp = Blueprint('main', __name__)

@bp.route('/welcome')
def welcome():
    return "<h1>Welcome!</h1>"

# @app.route('/recognize-from-file', methods=['POST'])
# def recognize_from_file():
#     if 'file' not in request.files:
#         return "No file part", 400
#
#     file = request.files['file']
#     if file.filename == '':
#         return "No selected file", 400
#
#     # 你可能需要保存文件并提供正确的路径
#     filename = './' + file.filename
#     file.save(filename)
#
#     result = speech_manager.recognize_speech_from_file(filename)
#     return jsonify(result=result)

@bp.route('/health', methods=['GET'])
def health_check():
    # 在这里，你可以添加任何必要的健康检查逻辑
    # 例如，检查数据库连接、外部服务的可用性等
    # 如果一切正常，返回一个正常的响应

    # 简单的响应，表明服务运行正常
    return jsonify(status="healthy", message="Service is up and running"), 200


@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        msg = request.get_json()
        print(msg)

        try:
            chat_id, txt, time_stamp = current_app.bot_manager.tel_parse_message(msg)
            if current_app.message_handler.is_gpt_entrance(txt):
                # change to the thread id user select
                thread_id=txt[1:]
                current_app.message_handler.set_thread_by_id(chat_id, thread_id)
                current_app.bot_manager.tel_send_message(chat_id, 'Chat thread successfully changed to selected meeting!')
            elif current_app.message_handler.is_command(txt):
                result=current_app.message_handler.execute_command(txt,chat_id)
                if result is not None:
                    current_app.bot_manager.tel_send_message(chat_id, result)
            else:
                # chat with gpt assistant
                current_thread=current_app.message_handler.get_thread_by_id(chat_id)
                if current_thread is None:
                    #start a new thread
                    current_thread=current_app.ai_agent.create_thread(chat_id,time_stamp)
                    current_app.message_handler.set_thread_by_id(chat_id,current_thread)
                # current_app.ai_agent.respond(chat_id,current_thread,txt)


                current_app.ai_agent.respond(chat_id,current_thread,txt)

        except Exception as e:
            print(f"A Exception occurred: {e}")


        try:
            chat_id, file_id, file_type = current_app.bot_manager.tel_parse_get_message(msg)

            file_path=current_app.bot_manager.tel_upload_file(file_id)
            if file_path is not None:
                current_app.bot_manager.tel_send_message(chat_id, "upload success")
                if file_type != FileType.AUDIO:
                    current_app.bot_manager.tel_send_message(chat_id,
                                                             "However, the bot doesn't support this type of file "
                                                             "at the moment")
                else:
                    current_app.message_handler.add_audio_to_chat_state(chat_id,file_path)
                    current_app.bot_manager.tel_send_language_option(chat_id)

            else:
                current_app.bot_manager.tel_send_message(chat_id, "upload failed, file size may exceeds the limit of bot capability(20MB)")


        except:
            print("No file from index-->")

        return Response('ok', status=200)
    else:
        return "<h1>Welcome!</h1>"
