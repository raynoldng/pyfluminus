import unittest

from pyfluminus.utils import sanitise_filename


class TestUtils(unittest.TestCase):

    def test_sanitise_filename(self):
        self.assertEquals(sanitise_filename("asd\0"), "asd-")
        self.assertEquals(sanitise_filename("asd/asd/asd"), "asd-asd-asd")
        self.assertEquals(sanitise_filename("\0asd/asd/asd"), "-asd-asd-asd")

        self.assertEquals(sanitise_filename("asd\0", "+"), "asd+")
        self.assertEquals(sanitise_filename("asd/asd/asd", "+"), "asd+asd+asd")
        self.assertEquals(sanitise_filename("\0asd/asd/asd", "+"), "+asd+asd+asd")
