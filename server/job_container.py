import job

class JobContainer:
    """
    A container for a single Job instance. It can be in either of two states,
    'complete' or 'running'.
    """

    def create_new(self, events_url):
        self._job = job.Job(events_url)

    def is_running(self):
        return hasattr(self, '_job')

    def is_complete(self):
        return not self.is_running()

    def complete(self):
        del self._job

    def get_events_url(self):
        return self._job.get_events_url()
