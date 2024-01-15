import json

from flask import Flask
from openai import OpenAI

from app.AIAgent import AIAgent
from app.BotManager import BotManager
from app.MessageHandler import MessageHandler
from app.SpeechService import SpeechService
from app.AssistantDBManager import AssistantDBManager
import os
from app.routes import bp as main_bp


def create_app():
    app = Flask(__name__)
    current_working_directory = os.getcwd()
    # load config file by env(prod, qa)
    env = os.environ.get('FLASK_ENV', 'QA').upper()
    if env == 'PROD':
        config_file = os.path.join(current_working_directory, 'config_prod.json')
    else:
        config_file = os.path.join(current_working_directory, 'config_qa.json')
    print(f"Application running in {env} version")

    # 加载 JSON 配置文件
    app.config.from_file(config_file, load=json.load)

    app.register_blueprint(main_bp)  # register blueprint

    # app.ai_client = OpenAI(api_key=app.config['OPENAI_API_KEY'])
    app.db_manager = AssistantDBManager(app.config['DATABASE_URI'])
    app.speech_service = SpeechService(subscription=app.config['SPEECH_KEY'], region=app.config['SPEECH_REGION'])
    app.bot_manager = BotManager(app.config['BOT_TOKEN'])
    app.message_handler = MessageHandler(app.config['BOT_TOKEN'])
    app.ai_agent = AIAgent(app.config['ASSISTANT_ID'], app.config['OPENAI_API_KEY'])

    return app
