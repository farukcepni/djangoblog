from djcelery import celery

@celery.task(name='farukcepni')
def create_thumbs(image):
    image._create_thumbs()
    return True