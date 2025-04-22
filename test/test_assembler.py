import unittest
from asmy.assembler import Assembler


class TestAssemblerCore(unittest.TestCase):
    def test_db(self):
        asm = Assembler()
        asm.db(0x01, 0x02, 0x03)
        self.assertEqual(bytes(asm.rom), b"\x01\x02\x03")
        asm.db(0x04)
        self.assertEqual(bytes(asm.rom), b"\x01\x02\x03\x04")

    def test_dw_le(self):
        asm = Assembler(endian="little")
        asm.dw(0x0102, 0x0304)
        self.assertEqual(bytes(asm.rom), b"\x02\x01\x04\x03")

    def test_dw_be(self):
        asm = Assembler(endian="big")
        asm.dw(0x0102, 0x0304)
        self.assertEqual(bytes(asm.rom), b"\x01\x02\x03\x04")

    def test_org(self):
        asm = Assembler()
        asm.org(0x100)
        self.assertEqual(len(asm.rom), 0x100)
        asm.db(0x01)
        self.assertEqual(bytes(asm.rom[0x100:0x101]), b"\x01")
        asm.org(0x200)
        self.assertEqual(len(asm.rom), 0x200)
        asm.db(0x02)
        self.assertEqual(bytes(asm.rom[0x200:0x201]), b"\x02")
        self.assertRaises(ValueError, asm.org, 0x150)

    def test_label_undefined(self):
        asm = Assembler()
        self.assertRaises(ValueError, asm.label("undefined").addr)

    def test_label_backward(self):
        asm = Assembler()
        asm.org(2)
        asm.db(1)
        with asm.label("start"):
            asm.db(42)
        self.assertEqual(asm.labels["start"], 3)
        self.assertEqual(bytes(asm.rom[0:4]), b"\x00\x00\x01\x2A")
        self.assertEqual(asm.label("start").addr(), 3)

    def test_label_forward(self):
        asm = Assembler()
        asm.org(2)
        with asm.label("start"):
            asm.dw(asm.label("end"))
        with asm.label("end"):
            asm.db(42)
        self.assertEqual(asm.label("start").addr(), 2)
        self.assertEqual(asm.label("end").addr(), 4)
        self.assertEqual(bytes(asm.rom[0:5]), b"\x00\x00\x04\x00\x2A")

    def test_pc_start(self):
        asm = Assembler(pc_start=0x100)
        asm.org(0x100)
        asm.db(0x01)
        self.assertEqual(bytes(asm.rom[:1]), b"\x01")
        asm.org(0x108)
        asm.db(0x02)
        self.assertEqual(bytes(asm.rom[8:9]), b"\x02")
        self.assertEqual(len(asm.rom), 9)


if __name__ == "__main__":
    unittest.main()
