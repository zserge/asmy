from .assembler import Assembler

asm = Assembler(endian='little', pc_start=0x8000)
L, org, db, dw = asm.Label, asm.org, asm.db, asm.dw

A, X, Y = 'A', 'X', 'Y'

def _op(code, mode, operand=None):
    opcode = _OPCODES[(code, mode)]
    if operand is not None:
        if isinstance(operand, Assembler.Label):
            asm._emit_label_ref(operand, 2 if mode in ('abs', 'abs,x') else 1)
        else:
            if mode in ('imm', 'zp'):
                asm.db(operand & 0xFF)
            elif mode == 'abs':
                asm.dw(operand & 0xFFFF)
    asm.db(opcode)

# Instruction set
def LDA(operand, mode='imm'):
    _op('LDA', mode, operand)

def STA(operand, mode='abs'):
    _op('STA', mode, operand)

def JMP(operand):
    _op('JMP', 'abs', operand)

# Opcode table (partial)
_OPCODES = {
    ('LDA', 'imm'): 0xA9,
    ('LDA', 'zp'): 0xA5,
    ('LDA', 'abs'): 0xAD,
    ('STA', 'abs'): 0x8D,
    ('JMP', 'abs'): 0x4C,
    # ... add more instructions
}
