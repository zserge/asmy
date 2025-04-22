import unittest
from asmy.gmc4 import *


class TestLMC(unittest.TestCase):
    def setUp(self):
        asm.reset()

    def test_demo_asc_numbers(self):
        with label("start"):
            tia(0)
        with label("again"):
            ao()
            ch()
        with label("wait-key"):
            ka()
            jump("wait-key")
            ch()
            aia(7)
        with label("loop"):
            jump("loop")  # if carry
            aia(0xA)
            ch()
        with label("key-pressed"):
            ka()
            jump("restore")
            jump("key-pressed")
        with label("restore"):
            ch()
            jump("again")

        print(mem(" "))
        self.assertEqual(mem(), "80120f04297f0b9a20f18f112f02")
