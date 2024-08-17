from celery import shared_task


@shared_task(bind=True)
def history(self, data=""):
    return f"ola mundo {data}"
