#!/usr/bin/env python3

job_completed = False


def complete_job():
    global job_completed
    job_completed = True


def is_complete():
    return job_completed
