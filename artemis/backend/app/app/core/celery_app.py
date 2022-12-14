from celery import Celery

celery_app = Celery(
    "worker", backend="redis://redis:6379/1", broker="pyamqp://guest:guest@queue//"
)

celery_app.conf.task_routes = {"app.worker.test_celery": "main-queue"}
