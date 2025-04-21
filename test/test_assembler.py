import unittest
from asmy.assembler import Assembler


class TestAssemblerCore(unittest.TestCase):
    def test_labels(self):
        asm = Assembler()
        with asm.label("start"):
            asm.db(0x90)
        self.assertEqual(asm.labels["start"], 0)

    def test_org(self):
        asm = Assembler()
        asm.org(0x100)
        self.assertEqual(len(asm.rom), 0x100)

    def test_db_dw(self):
        asm = Assembler()
        asm.db(0x01, 0x02)
        asm.dw(0x0304)
        self.assertEqual(bytes(asm.rom), b"\x01\x02\x04\x03")  # Little-endian

    def test_forward_label(self):
        asm = Assembler()
        asm.dw(asm.label("later") + 2)
        with asm.label("later"):
            asm.db(0xFF)
        rom = asm.finalize()
        self.assertEqual(rom[:2], b"\x02\x00")  # 0x0002 (little-endian)

    def test_backward_label(self):
        asm = Assembler()
        with asm.label("start"):
            asm.dw(asm.label("start"))
        rom = asm.finalize()
        self.assertEqual(rom[:2], b"\x00\x00")


if __name__ == "__main__":
    unittest.main()
