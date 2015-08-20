from unittest import TestCase

from remote_helper.job_container import JobContainer
from remote_helper.job import NullJob, Job

class JobContainerTest(TestCase):
    def setUp(self):
        self.a_job_container = JobContainer()

    def test_is_initialised_with_a_null_job(self):
        self.assertIs(type(self.a_job_container._job), NullJob)

    def test_creates_a_job_instance_when_create_new_job_is_called(self):
        self.a_job_container.create_new_job('some_url')

        self.assertIs(type(self.a_job_container._job), Job)

    def test_throws_away_old_instance_when_create_new_job_is_called(self):
        old_job = self.a_job_container._job

        self.a_job_container.create_new_job('some_url')

        self.assertIsNot(self.a_job_container._job, old_job)

    def test_exposes_the_currently_conatined_job(self):
        self.assertIs(self.a_job_container.get(), self.a_job_container._job)


if __name__ == '__main__':
    unittest.main()
