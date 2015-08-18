from server.job import Job, NullJob

class JobContainer:
    """
    A container for a single Job instance.
    """

    def __init__(self):
        self._job = NullJob()

    def create_new_job(self, events_url):
        self._job = Job(events_url)

    def get(self):
        return self._job
