import os


def environ(request):
    return {"APP_TITLE": os.getenv("APP_TITLE", "Django-Compose")}
