# chip8.py
from .assembler import Assembler

asm = Assembler(endian='big', pc_start=0x200)
L = lambda name: asm.Label(name, asm)
org, db, dw = asm.org, asm.db, asm.dw

V0, V1, V2, V3, V4, V5, V6, V7, V8, V9, VA, VB, VC, VD, VE, VF = range(16)

def _emit(op, x=0, y=0, n=0, nnn=0):
    instr = (op << 12) | (x << 8) | (y << 4) | n
    asm.rom += instr.to_bytes(2, 'big')
    asm.pc += 2

def CLS(): _emit(0x00E0)
def RET(): _emit(0x00EE)
def SYS(addr): _emit(0x0, nnn=addr)
def JP(addr): _emit(0x1, nnn=addr)
def CALL(addr): _emit(0x2, nnn=addr)
def SE(x, kk): _emit(0x3, x=x, n=kk)
# ... add all 34 instructions following same pattern

def DRW(x, y, n):
    _emit(0xD, x=x, y=y, n=n)
