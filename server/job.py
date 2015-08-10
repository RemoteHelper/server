class Job:
    def __init__(self, events_url):
        self._events_url = events_url

    def get_events_url(self):
        return self._events_url
