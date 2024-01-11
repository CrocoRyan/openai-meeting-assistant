import threading
import queue
import time

# 创建消息队列
message_queue = queue.Queue()

def process_messages():
    while True:
        message = message_queue.get()
        print(f"Processing message: {message}")
        # 这里添加处理消息的逻辑
        time.sleep(1)  # 模拟处理延时
        message_queue.task_done()

def start_background_thread():
    t = threading.Thread(target=process_messages)
    t.daemon = True
    t.start()
