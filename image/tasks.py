from djcelery import celery

@celery.task(name='task_create_thumbs')
def create_thumbs(image):
    image._create_thumbs()
    return True