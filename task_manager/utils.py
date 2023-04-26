from django.test import modify_settings


class disable_rollbar(modify_settings):
    '''Decorator for disabling rollbar during the tests'''
    middleware = {'remove': ['rollbar.contrib.django.middleware.RollbarNotifierMiddleware']}

    def __init__(self, *args, **kwargs):
        kwargs.update({'MIDDLEWARE': self.middleware})
        super().__init__(**kwargs)
