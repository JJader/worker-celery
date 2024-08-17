from celery import shared_task


@shared_task(
    bind=True,
)
def load(self, data=""):
    return f"ola mundo {data}"


@shared_task(
    bind=True,
)
def predict(self, data=""):
    return f"ola mundo {data}"
