import app.message_queue.huey_tasks  # pylint: disable=unused-import
from app import message_queue

if __name__ == '__main__':
    message_queue.consumer.run()
