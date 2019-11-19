import logging
import os
from unittest import skipUnless

import requests
from django.test import TestCase

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logging.basicConfig()


class UnitTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super(UnitTests, cls).setUpClass()
        cls.live_host = "%s:%s" % (os.getenv('FRONTEND_HOST', 'localhost'), os.getenv('FRONTEND_PORT', '8000'))

    def test_ping_unit(self):
        logger.info("testing ping by using Django client")
        response = self.client.get('/ping')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"pong")

    @skipUnless(os.getenv('CI') is not None, "not in CI")
    def test_ping_integration(self):
        logger.info("testing ping by sending request to a frontend in a CI environment")
        response = requests.get('http://%s/ping' % self.live_host)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"pong")

    @skipUnless(os.getenv('CI') is not None, "not in CI")
    def test_sync_task_integration(self):
        logger.info("testing sync_task by sending request to a frontend in a CI environment")
        response = requests.get('http://%s/api/hash/test' % self.live_host)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"bc89c6f72947bcd2f783d342a46cafcfccfcc2e7884a34f1cfe8f55bad2d200e")

    def test_unhandled_exception(self):
        pass
        # raise Exception("Something really bad happened")


import random  # noqa


class BrokenFixedTests(TestCase):
    pass


fixed = random.choice((0, 1)) == 0


for n in range(50):
    name = f'test_{n}'

    def func(self):
        if fixed:
            return

        errored = random.choice((0, 1)) == 0
        if errored:
            raise ValueError("BOOOOM!")
        # else failed
        self.assertEqual(0, 1)

    func.__name__ = name
    setattr(BrokenFixedTests, name, func)
