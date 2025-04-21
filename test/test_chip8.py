import unittest
from asmy.chip8 import asm, JP, CLS, L

class TestChip8(unittest.TestCase):
    def setUp(self):
        asm.rom.clear()
        asm.pc = 0x200
        asm.labels.clear()
        asm.fixups.clear()

    def test_jp_instruction(self):
        JP(L('target'))
        with L('target'):
            CLS()
        rom = asm.finalize()
        self.assertEqual(rom[0:2], bytes.fromhex('1302'))
        
    def test_data_org(self):
        asm.org(0x200)
        asm.db(0x12, 0x34)
        self.assertEqual(bytes(asm.rom[0x200:0x202]), b'\x12\x34')

if __name__ == '__main__':
    unittest.main()
