from djcelery import celery


def testing(x, y):
    return x + y

@celery.task(name='farukcepni')
def add(x, y):
    import datetime
    a = datetime.datetime.now().microsecond
    return 10
