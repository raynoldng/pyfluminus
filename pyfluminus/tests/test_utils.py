import unittest

from pyfluminus.utils import sanitise_filename


class TestUtils(unittest.TestCase):

    def test_sanitise_filename(self):
        # replaces both nil and / with -
        self.assertEquals(sanitise_filename("asd\0"), "asd-")
        self.assertEquals(sanitise_filename("asd/asd/asd"), "asd-asd-asd")
        self.assertEquals(sanitise_filename("\0asd/asd/asd"), "-asd-asd-asd")

        # works with other replacement
        self.assertEquals(sanitise_filename("asd\0", "+"), "asd+")
        self.assertEquals(sanitise_filename("asd/asd/asd", "+"), "asd+asd+asd")
        self.assertEquals(sanitise_filename("\0asd/asd/asd", "+"), "+asd+asd+asd")
