import unittest
from asmy.sweet16 import *


class TestSweet16(unittest.TestCase):
    def setUp(self):
        asm.reset()

    def test_demo(self):
        with label("init"):
            SET(R0, 0)
            SET(R1, 1)
            SET(R2, 2)
            ADD(R1)
            ST(R3)
            SUB(R2)
            ST(R4)
            BM1("L2")
        with label("L1"):
            SET(R5, 0)
            BK()
        with label("L2"):
            SET(R5, 0x1004)
            RTN()
        self.assertEqual(
            asm.rom.hex(" "),
            "10 00 00 11 01 00 12 02 00 a1 33 b2 34 08 04 15 00 00 0a 15 04 10 00",
        )

    def test_memcpy(self):
        with label("loop"):
            LD([R1])
            ST([R2])
            DCR(R3)
            BNZ("loop")
            RTN()
        self.assertEqual(asm.rom.hex(" "), "41 52 f3 07 fb 00")
