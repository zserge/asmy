import unittest
from asmy.mos6502 import *


class TestMOS6502(unittest.TestCase):
    def setUp(self):
        asm.reset()

    def test_implied(self):
        with label("start"):
            BRK()
            CLC()
            CLD()
            CLI()
            CLV()
            DEX()
            DEY()
            INX()
            INY()
            NOP()
            PHA()
            PHP()
            PLA()
            PLP()
            RTI()
            RTS()
            SEC()
            SED()
            SEI()
            TAX()
            TAY()
            TSX()
            TXA()
            TXS()
            TYA()
        self.assertEqual(
            asm.rom.hex(" "),
            "00 18 d8 58 b8 ca 88 e8 c8 ea 48 08 68 28 40 60 38 f8 78 aa a8 ba 8a 9a 98",
        )

    def test_lda(self):
        with label("start"):
            LDA(I @ 0x42)  # immediate mode
            LDA(0x42)  # zero page
            LDA(0x42, X)  # zero page, X
            LDA(0x1234)  # absolute
            LDA(0x1234, X)  # absolute,X
            LDA(0x1234, Y)  # absolute,Y
            LDA([0x34, X])  # indirect,X
            LDA([0x34], Y)  # indirect,Y
        self.assertEqual(
            asm.rom.hex(" "), "a9 42 a5 42 b5 42 ad 34 12 bd 34 12 b9 34 12 a1 34 b1 34"
        )

    def test_ldx(self):
        with label("start"):
            LDX(I @ 0x42)
            LDX(0x42)
            LDX(0x42, Y)
            LDX(0x1234)
        self.assertEqual(asm.rom.hex(" "), "a2 42 a6 42 b6 42 ae 34 12")

    def test_ldy(self):
        with label("start"):
            LDY(I @ 0x42)
            LDY(0x42)
            LDY(0x42, X)
            LDY(0x1234)
        self.assertEqual(asm.rom.hex(" "), "a0 42 a4 42 b4 42 ac 34 12")

    def test_sta(self):
        with label("start"):
            STA(0x42)
            STA(0x42, X)
            STA(0x1234)
            STA(0x1234, X)
            STA(0x1234, Y)
            STA([0x34, X])
            STA([0x34], Y)
        self.assertEqual(
            asm.rom.hex(" "), "85 42 95 42 8d 34 12 9d 34 12 99 34 12 81 34 91 34"
        )

    def test_stx(self):
        with label("start"):
            STX(0x42)
            STX(0x42, Y)
            STX(0x1234)
        self.assertEqual(asm.rom.hex(" "), "86 42 96 42 8e 34 12")

    def test_sty(self):
        with label("start"):
            STY(0x42)
            STY(0x42, X)
            STY(0x1234)
        self.assertEqual(asm.rom.hex(" "), "84 42 94 42 8c 34 12")

    def test_adc(self):
        with label("start"):
            ADC(I @ 0x42)
            ADC(0x42)
            ADC(0x42, X)
            ADC(0x1234)
            ADC(0x1234, X)
            ADC(0x1234, Y)
            ADC([0x34, X])
            ADC([0x34], Y)
        self.assertEqual(
            asm.rom.hex(" "),
            "69 42 65 42 75 42 6d 34 12 7d 34 12 79 34 12 61 34 71 34",
        )

    def test_sbc(self):
        with label("start"):
            SBC(I @ 0x42)
            SBC(0x42)
            SBC(0x42, X)
            SBC(0x1234)
            SBC(0x1234, X)
            SBC(0x1234, Y)
            SBC([0x34, X])
            SBC([0x34], Y)
        self.assertEqual(
            asm.rom.hex(" "),
            "e9 42 e5 42 f5 42 ed 34 12 fd 34 12 f9 34 12 e1 34 f1 34",
        )

    def test_cmp(self):
        with label("start"):
            CMP(I @ 0x42)
            CMP(0x42)
            CMP(0x42, X)
            CMP(0x1234)
            CMP(0x1234, X)
            CMP(0x1234, Y)
            CMP([0x34, X])
            CMP([0x34], Y)
        self.assertEqual(
            asm.rom.hex(" "),
            "c9 42 c5 42 d5 42 cd 34 12 dd 34 12 d9 34 12 c1 34 d1 34",
        )

    def test_cpx(self):
        with label("start"):
            CPX(I @ 0x42)
            CPX(0x42)
            CPX(0x1234)
        self.assertEqual(asm.rom.hex(" "), "e0 42 e4 42 ec 34 12")

    def test_cpy(self):
        with label("start"):
            CPY(I @ 0x42)
            CPY(0x42)
            CPY(0x1234)
        self.assertEqual(asm.rom.hex(" "), "c0 42 c4 42 cc 34 12")

    def test_inc(self):
        with label("start"):
            INC(0x42)
            INC(0x42, X)
            INC(0x1234)
        self.assertEqual(asm.rom.hex(" "), "e6 42 f6 42 ee 34 12")

    def test_dec(self):
        with label("start"):
            DEC(0x42)
            DEC(0x42, X)
            DEC(0x1234)
        self.assertEqual(asm.rom.hex(" "), "c6 42 d6 42 ce 34 12")

    def test_asl(self):
        with label("start"):
            ASL(0x42)
            ASL(0x42, X)
            ASL(0x1234)
            ASL(A)
        self.assertEqual(asm.rom.hex(" "), "06 42 16 42 0e 34 12 0a")

    def test_lsr(self):
        with label("start"):
            LSR(0x42)
            LSR(0x42, X)
            LSR(0x1234)
            LSR(A)
        self.assertEqual(asm.rom.hex(" "), "46 42 56 42 4e 34 12 4a")

    def test_rol(self):
        with label("start"):
            ROL(0x42)
            ROL(0x42, X)
            ROL(0x1234)
            ROL(A)
        self.assertEqual(asm.rom.hex(" "), "26 42 36 42 2e 34 12 2a")

    def test_ror(self):
        with label("start"):
            ROR(0x42)
            ROR(0x42, X)
            ROR(0x1234)
            ROR(A)
        self.assertEqual(asm.rom.hex(" "), "66 42 76 42 6e 34 12 6a")

    def test_bit(self):
        with label("start"):
            BIT(0x42)
            BIT(0x1234)
        self.assertEqual(asm.rom.hex(" "), "24 42 2c 34 12")

    def test_and(self):
        with label("start"):
            AND(I @ 0x42)
            AND(0x42)
            AND(0x42, X)
            AND(0x1234)
            AND(0x1234, X)
            AND(0x1234, Y)
            AND([0x34, X])
            AND([0x34], Y)
        self.assertEqual(
            asm.rom.hex(" "),
            "29 42 25 42 35 42 2d 34 12 3d 34 12 39 34 12 21 34 31 34",
        )

    def test_eor(self):
        with label("start"):
            EOR(I @ 0x42)
            EOR(0x42)
            EOR(0x42, X)
            EOR(0x1234)
            EOR(0x1234, X)
            EOR(0x1234, Y)
            EOR([0x34, X])
            EOR([0x34], Y)
        self.assertEqual(
            asm.rom.hex(" "),
            "49 42 45 42 55 42 4d 34 12 5d 34 12 59 34 12 41 34 51 34",
        )

    def test_ora(self):
        with label("start"):
            ORA(I @ 0x42)
            ORA(0x42)
            ORA(0x42, X)
            ORA(0x1234)
            ORA(0x1234, X)
            ORA(0x1234, Y)
            ORA([0x34, X])
            ORA([0x34], Y)
        self.assertEqual(
            asm.rom.hex(" "),
            "09 42 05 42 15 42 0d 34 12 1d 34 12 19 34 12 01 34 11 34",
        )

    def test_jmp(self):
        with label("start"):
            JMP(0x1234)
            JMP([0x1234])
            JSR(0x1234)
        self.assertEqual(asm.rom.hex(" "), "4c 34 12 6c 34 12 20 34 12")

    def test_branch(self):
        with label("start"):
            BCC("start")
            BCS("end")
            BEQ("start")
            BMI("end")
            BNE("start")
            BPL("end")
            BVC("start")
            BVS("end")
            JMP("start")
        with label("end"):
            JSR("end")
        self.assertEqual(
            asm.rom.hex(" "),
            "90 fe b0 0f f0 fa 30 0b d0 f6 10 07 50 f2 70 03 4c 00 00 20 13 00",
        )
