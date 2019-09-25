import time
from celery import Celery

""" def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery """

app = Celery('tasks', backend='redis://localhost', broker='redis://localhost:6379')

@app.task(bind=True)
def get_quote(self, parts_to_quote: list):
    parts_info = []
    total = len(parts_to_quote)
    for idx, part in enumerate(parts_to_quote):
        print(part)
        self.update_state(
            state='PROGRESS',
            meta={
                'completed': idx,
                'total': total
            }
        )
        parts_info.append(part)
        time.wait(5)
    return parts_info