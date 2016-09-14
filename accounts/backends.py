from django.contrib.auth.backends import ModelBackend as BaseModelBackend


class ModelBackend(BaseModelBackend):
    def authenticate(self, username=None, password=None):
        if username is None:
            pass