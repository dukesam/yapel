
class YapelApiError(Exception):
    def __init__(self, api_error, *args, **kwargs):
        super(YapelApiError, self).__init__(*args, **kwargs)
        self.api_error = api_error