from .assembler import Assembler

asm = Assembler(endian="little", pc_start=0x8000)
L, org, db, dw = asm.Label, asm.org, asm.db, asm.dw

A, X, Y = "A", "X", "Y"


def _op(code, mode, operand=None):
    opcode = _OPCODES[(code, mode)]
    if operand is not None:
        if isinstance(operand, Assembler.Label):
            asm._emit_label_ref(operand, 2 if mode in ("abs", "abs,x") else 1)
        else:
            if mode in ("imm", "zp"):
                asm.db(operand & 0xFF)
            elif mode == "abs":
                asm.dw(operand & 0xFFFF)
    asm.db(opcode)


# Instruction set
def LDA(operand, mode="imm"):
    _op("LDA", mode, operand)


def STA(operand, mode="abs"):
    _op("STA", mode, operand)


def JMP(operand):
    _op("JMP", "abs", operand)


# Opcode table (partial)
_OPCODES = {
    ("LDA", "imm"): 0xA9,
    ("LDA", "zp"): 0xA5,
    ("LDA", "abs"): 0xAD,
    ("STA", "abs"): 0x8D,
    ("JMP", "abs"): 0x4C,
    # ... add more instructions
}

# ADC add with carry
# AND and (with accumulator)
# ASL arithmetic shift left
# BCC branch on carry clear
# BCS branch on carry set
# BEQ branch on equal (zero set)
# BIT bit test
# BMI branch on minus (negative set)
# BNE branch on not equal (zero clear)
# BPL branch on plus (negative clear)
# BRK break / interrupt
# BVC branch on overflow clear
# BVS branch on overflow set
# CLC clear carry
# CLD clear decimal
# CLI clear interrupt disable
# CLV clear overflow
# CMP compare (with accumulator)
# CPX compare with X
# CPY compare with Y
# DEC decrement
# DEX decrement X
# DEY decrement Y
# EOR exclusive or (with accumulator)
# INC increment
# INX increment X
# INY increment Y
# JMP jump
# JSR jump subroutine
# LDA load accumulator
# LDX load X
# LDY load Y
# LSR logical shift right
# NOP no operation
# ORA or with accumulator
# PHA push accumulator
# PHP push processor status (SR)
# PLA pull accumulator
# PLP pull processor status (SR)
# ROL rotate left
# ROR rotate right
# RTI return from interrupt
# RTS return from subroutine
# SBC subtract with carry
# SEC set carry
# SED set decimal
# SEI set interrupt disable
# STA store accumulator
# STX store X
# STY store Y
# TAX transfer accumulator to X
# TAY transfer accumulator to Y
# TSX transfer stack pointer to X
# TXA transfer X to accumulator
# TXS transfer X to stack pointer
# TYA transfer Y to accumulator
