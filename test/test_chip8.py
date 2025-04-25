import unittest
from asmy.chip8 import *


class TestChip8(unittest.TestCase):
    def setUp(self):
        asm.reset()

    def test_endless_loop(self):
        with label("start"):
            cls()
            jp("start")
        with label("data"):
            db(0b01010101)
            db(0b10101010)
        asm.finalize()
        self.assertEqual(asm.rom.hex(), "00e0 1200 55aa".replace(" ", ""))

    def test_uppercase(self):
        with label("start"):
            CLS()
            JP("start")

    def test_maze(self):
        # V0: X-coordinate of the bitmap
        # V1: Y-coordinate of the bitmap
        # V2: Random number
        with label("init"):
            ld(V0, 0)  # 6000
            ld(V1, 0)  # 6100
        with label("loop"):
            ld(I, "left")  # a222
            rnd(V2, 1)  # c201
            se(V2, 1)  # 3201
            ld(I, "right")  # a21e
            drw(V0, V1, 4)  # d014
            add(V0, 4)  # 7004
            se(V0, 64)  # 3040
            jp("loop")  # 1204
            ld(V0, 0)  # 6000
            add(V1, 4)  # 7104
            se(V1, 32)  # 3120
            jp("loop")  # 1204
        with label("fin"):
            jp("fin")  # 121c
        with label("right"):
            db(0b10000000)  # 80
            db(0b01000000)  # 40
            db(0b00100000)  # 20
            db(0b00010000)  # 10
        with label("left"):
            db(0b00100000)  # 20
            db(0b01000000)  # 40
            db(0b10000000)  # 80
            db(0b00010000)  # 10
        asm.finalize()
        s = asm.rom.hex()
        self.assertEqual(
            asm.rom.hex(),
            "".join(
                """
        6000 6100 a222 c201 3201 a21e d014 7004
        3040 1204 6000 7104 3120 1204 121c
        8040 2010 2040 8010         
        """.split()
            ),
        )


if __name__ == "__main__":
    unittest.main()
