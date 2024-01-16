from utils.constants import FileType


def text_progress_bar(progress, total, bar_length=10):
    # calculate the completed share of the entire task
    filled_length = int(bar_length * progress // total)

    # create progress blocks
    bar = "█" * filled_length
    bar += "-" * (bar_length - filled_length)

    return f"[ {bar} ] {int(100 * (progress / total))}%"
def split_gpt_text(message:str):
    message=message.strip('"')
    return message.split("\n")

def is_callback(message):
    return message.get('callback_query') is not None
def get_message_type(message):
    message=message['message']
    if message.get('text') is not None or message.get('callback_query') is not None:
        return FileType.TEXT
    if message.get('audio') is not None:
        return FileType.AUDIO
    if message.get('document') is not None:
        return FileType.OTHERS
    if message.get('video') is not None:
        return FileType.VIDEO
    if message.get('photo') is not None:
        return FileType.PHOTO
