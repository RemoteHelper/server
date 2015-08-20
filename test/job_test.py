from unittest import TestCase

from server.job import Job, NullJob

class JobTest(TestCase):
    def setUp(self):
        self.sample_events_url = 'http://url.to.some/events/endpoint'
        self.a_job = Job(self.sample_events_url)

    def test_is_running_right_after_creation(self):
        self.assertTrue(self.a_job.is_running())

    def test_is_not_complete_right_after_creation(self):
        self.assertFalse(self.a_job.is_complete())

    def test_is_not_resolved_right_after_creation(self):
        self.assertFalse(self.a_job.is_resolved())

    def test_can_be_switched_from_running_to_complete_status(self):
        self.assertFalse(self.a_job.is_complete())

        self.a_job.complete()

        self.assertTrue(self.a_job.is_complete())

    def test_is_not_running_when_in_complete_status(self):
        self.a_job.complete()

        self.assertFalse(self.a_job.is_running())

    def test_can_be_switched_from_complete_to_resolved_status(self):
        self.a_job.complete()
        self.assertTrue(self.a_job.is_complete())

        self.a_job.resolve()

        self.assertTrue(self.a_job.is_resolved())

    def test_switching_from_running_to_resolved_status_does_not_work(self):
        self.assertTrue(self.a_job.is_running())

        self.a_job.resolve()

        self.assertFalse(self.a_job.is_resolved())
        self.assertTrue(self.a_job.is_running())

    def test_is_not_running_when_in_resolved_status(self):
        self.a_job.complete()
        self.a_job.resolve()

        self.assertTrue(self.a_job.is_resolved())
        self.assertFalse(self.a_job.is_running())

    def test_can_be_asked_for_its_done_status(self):
        self.assertIs(type(self.a_job.done_status), dict)

    def test_its_done_status_is_false_if_in_running_state(self):
        self.assertTrue(self.a_job.is_running())

        done_status = self.a_job.done_status

        self.assertFalse(done_status['done'])

    def test_its_done_status_is_true_if_in_complete_state(self):
        self.a_job.complete()
        self.assertTrue(self.a_job.is_complete())

        done_status = self.a_job.done_status

        self.assertTrue(done_status['done'])

    def test_its_done_status_is_true_if_in_resolved_state(self):
        self.a_job.complete()
        self.a_job.resolve()
        self.assertTrue(self.a_job.is_resolved())

        done_status = self.a_job.done_status

        self.assertTrue(done_status['done'])

    def test_its_done_status_contains_the_done_text_if_it_has_been_prevously_set(self):
        some_done_text = 'some done text'
        self.a_job.done_text = some_done_text

        done_status = self.a_job.done_status

        self.assertIs(done_status['doneText'], some_done_text)

    def test_has_no_done_text_right_after_creation(self):
        self.assertFalse(hasattr(self.a_job, '_done_text'))

    def test_can_be_queried_to_tell_wether_it_has_a_done_text(self):
        self.a_job.done_text = 'some text'

        self.assertTrue(self.a_job.has_done_text())


class NullJobTest(TestCase):
    def setUp(self):
        self.a_null_job = NullJob()

    def test_is_not_running_right_after_creation(self):
        self.assertFalse(self.a_null_job.is_running())

    def test_is_complete_right_after_creation(self):
        self.assertTrue(self.a_null_job.is_complete())

    def test_is_resolved_right_after_creation(self):
        self.assertTrue(self.a_null_job.is_resolved())
