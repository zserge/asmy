from .assembler import Assembler

asm = Assembler(endian="big", pc_start=0x200)
label = lambda name: asm.label(name)
org, db, dw = asm.org, asm.db, asm.dw

V0, V1, V2, V3, V4, V5, V6, V7, V8, V9, VA, VB, VC, VD, VE, VF = [
    f"V{x}" for x in "0123456789ABCDEF"
]
I, DT, ST, HF, K, R = "I", "DT", "ST", "HF", "K", "R"


def _isreg(r):
    return isinstance(r, str) and r.upper() in {f"V{x}" for x in "0123456789ABCDEF"}


def _reg(r):
    if not _isreg(r):
        raise ValueError(f"Invalid register: {r}")
    return int(r[1], 16)


def _patch(op):
    return lambda rom, pos, addr: rom.__setitem__(
        slice(pos, pos + 2), (op | (addr & 0xFFF)).to_bytes(2, "big")
    )


def _is_label(x):
    return isinstance(x, str) and not _isreg(x)


def add(x, y):
    """
    ADD I, Vx       Fx1E
    ADD Vx, Vy      8xy4
    ADD Vx, byte    7xkk
    """
    if _isreg(x):
        if y == I:
            dw(0xF01E | (_reg(x) << 8))
        elif _isreg(y):
            dw(0x8004 | (_reg(x) << 8) | (_reg(y) << 4))
        elif isinstance(y, int):
            dw(0x7000 | (_reg(x) << 8) | (y & 0xFF))
        else:
            raise ValueError("Invalid add operands")
    else:
        raise ValueError("Invalid add destination")


def band(x, y):
    """
    AND Vx, Vy      8xy2
    """
    dw(0x8002 | (_reg(x) << 8) | (_reg(y) << 4))


def call(addr):
    """
    CALL addr       2nnn
    """
    if _is_label(addr):
        asm.fixup(addr, 2, _patch(0x2000))
    else:
        dw(0x2000 | (addr & 0xFFF))


def cls():
    """
    CLS             00E0
    """
    dw(0x00E0)


def drw(x, y, n=0):
    """
    DRW Vx, Vy, 0   Dxy0
    DRW Vx, Vy, n   Dxyn
    """
    dw(0xD000 | (_reg(x) << 8) | (_reg(y) << 4) | (n & 0xF))


def jp(addr, v0=None):
    """
    JP addr, V0     Bnnn
    JP addr         1nnn
    """
    if v0 is not None:
        if not v0 == V0:
            raise ValueError("Invalid JP V0, addr")
        if _is_label(addr):
            asm.fixup(addr, 2, _patch(0xB000))
        else:
            dw(0xB000 | (addr & 0xFFF))
    elif _is_label(addr):
        asm.fixup(addr, 2, _patch(0x1000))
    elif isinstance(addr, int):
        dw(0x1000 | (addr & 0xFFF))
    else:
        raise ValueError(f"Invalid JP address: {addr}")


def ld(x, y):
    """
    LD Vx, byte     6xkk
    LD Vx, Vy       8xy0
    LD Vx, DT       Fx07
    LD Vx, K        Fx0A
    LD Vx, R        Fx85
    LD Vx, I*       Fx65
    LD I*, Vx       Fx55
    LD I,  addr     Annn
    LD F,  Vx       Fx29
    LD B,  Vx       Fx33
    LD DT, Vx       Fx15
    LD ST, Vx       Fx18
    LD HF, Vx       Fx30
    LD R,  Vx       Fx75
    """
    if _isreg(x):
        if isinstance(y, int):
            dw(0x6000 | (_reg(x) << 8) | (y & 0xFF))
        elif _isreg(y):
            dw(0x8000 | (_reg(x) << 8) | (_reg(y) << 4))
        elif y == DT:
            dw(0xF007 | (_reg(x) << 8))
        elif y == K:
            dw(0xF00A | (_reg(x) << 8))
        elif y == R:
            dw(0xF085 | (_reg(x) << 8))
        elif y == I:
            dw(0xF065 | (_reg(x) << 8))
        else:
            raise ValueError("Invalid ld source for register")
    elif x == I:
        if _isreg(y):
            dw(0xF055 | (_reg(y) << 8))
        elif _is_label(y):
            asm.fixup(y, 2, _patch(0xA000))
        elif isinstance(y, int):
            dw(0xA000 | (y & 0xFFF))
        else:
            raise ValueError("Invalid ld destination I")
    elif x == F:
        dw(0xF029 | (_reg(y) << 8))
    elif x == B:
        dw(0xF033 | (_reg(y) << 8))
    elif x == DT:
        dw(0xF015 | (_reg(y) << 8))
    elif x == ST:
        dw(0xF018 | (_reg(y) << 8))
    elif x == HF:
        dw(0xF030 | (_reg(y) << 8))
    elif x == R:
        dw(0xF075 | (_reg(y) << 8))
    else:
        raise ValueError("Invalid ld operands")


def bor(x, y):
    """
    OR Vx, Vy       8xy1
    """
    dw(0x8001 | (_reg(x) << 8) | (_reg(y) << 4))


def ret():
    """
    RET             00EE
    """
    dw(0x00EE)


def rnd(x, n):
    """
    RND Vx, byte    Cxkk
    """
    dw(0xC000 | (_reg(x) << 8) | (n & 0xFF))


def se(x, y):
    """
    SE Vx, Vy       5xy0
    SE Vx, byte     3xkk
    """
    if _isreg(x) and _isreg(y):
        dw(0x5000 | (_reg(x) << 8) | (_reg(y) << 4))
    elif _isreg(x) and isinstance(y, int):
        dw(0x3000 | (_reg(x) << 8) | (y & 0xFF))
    else:
        raise ValueError("Invalid operands for se")


def shl(x, y=0):
    """
    SHL Vx {, Vy}   8xyE
    """
    dw(0x800E | (_reg(x) << 8) | (_reg(y) << 4))


def shr(x, y=0):
    """
    SHR Vx {, Vy}   8xy6
    """
    dw(0x8006 | (_reg(x) << 8) | (_reg(y) << 4))


def sknp(x):
    """
    SKNP Vx         ExA1
    """
    dw(0xE0A1 | (_reg(x) << 8))


def skp(x):
    """
    SKP Vx          Ex9E
    """
    dw(0xE09E | (_reg(x) << 8))


def sne(x, y):
    """
    SNE Vx, Vy      9xy0
    SNE Vx, byte    4xkk
    """
    if _isreg(x) and _isreg(y):
        dw(0x9000 | (_reg(x) << 8) | (_reg(y) << 4))
    elif _isreg(x) and isinstance(y, int):
        dw(0x4000 | (_reg(x) << 8) | (y & 0xFF))
    else:
        raise ValueError("Invalid operands for sne")


def sub(x, y):
    """
    SUB Vx, Vy      8xy5
    """
    dw(0x8005 | (_reg(x) << 8) | (_reg(y) << 4))


def subn(x, y):
    """
    SUBN Vx, Vy     8xy7
    """
    dw(0x8007 | (_reg(x) << 8) | (_reg(y) << 4))


#  SYS addr               0nnn


def xor(x, y):
    """
    XOR Vx, Vy      8xy3
    """
    dw(0x8003 | (_reg(x) << 8) | (_reg(y) << 4))


#
# SCHIP instructions
#


def scd(n):
    """SCD nibble  00Cn"""
    dw(0x00C0 | (n & 0xF))


def scr():
    """SCR         00FB"""
    dw(0x00FB)


def scl():
    """SCL         00FC"""
    dw(0x00FC)


def exit():
    """EXIT        00FD"""
    dw(0x00FD)


def low():
    """LOW         00FE"""
    dw(0x00FE)


def high():
    """HIGH        00FF"""
    dw(0x00FF)


# fmt: off
ADD, AND, CALL, CLS, DRW, JP, LD, OR, RET, RND, SE, SHL, SHR, SKNP, SKP, SNE, SUB, SUBN, XOR = add, band, call, cls, drw, jp, ld, bor, ret, rnd, se, shl, shr, sknp, skp, sne, sub, subn, xor
