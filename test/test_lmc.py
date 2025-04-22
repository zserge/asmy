import unittest
from asmy.lmc import *


class TestLMC(unittest.TestCase):
    def setUp(self):
        asm.reset()

    def test_countdown(self):
        with label("start"):  # mailbox 0
            inp()
        with label("loop"):  # mailbox 1
            out()
            sta("count")
            sub("one")
            sta("count")
            brp("loop")
            hlt()
        with label("one"):  # mailbox 7
            dat(1)
        with label("count"):  # mailbox 8
            dat()
        self.assertEqual(mem(), [901, 902, 308, 207, 308, 801, 0, 1, 0])
