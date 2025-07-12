from celery import Celery

celery_app = Celery('worker', broker='redis://localhost:6379/0')

@celery_app.task
def gemini_task(chatroom_id, message_id, content):
    # Call Gemini API here
    # For example:
    # response = call_gemini_api(content)
    # Save response to database, etc.
    pass
