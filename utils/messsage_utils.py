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
