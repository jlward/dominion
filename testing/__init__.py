from unittest import TestCase

from faker import Faker


class BaseTestCase(TestCase):
    faker = Faker()
