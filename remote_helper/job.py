class Job:
    """
        The help job being processed by the remote helper.
        It has three states, described by the tuple
        (self._complete, self._resolved):
            running:  (False, False)
            complete: (True, False)
            resolved: (True, True)

        It is created in 'started' state, can then be switched
        to 'complete' state, and is only switched to 'resolved'
        state when it is queried for its status and it has
        already been completed.
    """
    def __init__(self, events_url):
        self._events_url = events_url
        self._complete = False
        self._resolved = False

    @property
    def events_url(self):
        return self._events_url

    @property
    def done_text(self):
        return self._done_text

    @done_text.setter
    def done_text(self, given_done_text):
        self._done_text = given_done_text

    def is_running(self):
        return not self._complete and not self._resolved

    def is_complete(self):
        return self._complete

    def complete(self):
        self._complete = True

    def is_resolved(self):
        return self._resolved

    def resolve(self):
        if self.is_running():
            return

        self._resolved = True

    @property
    def done_status(self):
        job_status = {
            'done': self.is_complete()
        }

        if self.has_done_text():
            job_status['doneText'] = self.done_text

        return job_status

    def has_done_text(self):
        return hasattr(self, '_done_text')



class NullJob(Job):
    def __init__(self):
        self._events_url = ''
        self._complete = True
        self._resolved = True
