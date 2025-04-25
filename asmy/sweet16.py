from .assembler import Assembler

asm = Assembler(endian="big", pc_start=0)
label = lambda name: asm.label(name)
org, db = asm.org, asm.db


R0, R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15 = range(16)


def _is_reg(r):
    return isinstance(r, int) and 0 <= r <= 0x0F


def _emit_byte(b):
    db(b & 0xFF)


def _fixup_branch(opcode, label_name):
    """Fixup for two-byte relative branches."""

    def patch(rom, pos, target_addr):
        rom[pos] = (target_addr - pos - 1) & 0xFF

    asm.db(opcode)
    asm.fixup(label_name, 1, patch)


def rtn():
    _emit_byte(0x00)


def setr(r, val):
    """SET Rn: load 16-bit constant into Rn."""
    if not _is_reg(r):
        raise ValueError(f"Bad register: {r}")
    _emit_byte(0x10 | r)
    _emit_byte(val & 0xFF)
    _emit_byte((val >> 8) & 0xFF)


def ld(arg):
    """LD Rn or LD @Rn (indirect)"""
    if _is_reg(arg):
        _emit_byte(0x20 | arg)
    elif isinstance(arg, list) and _is_reg(arg[0]):
        _emit_byte(0x40 | arg[0])
    else:
        raise ValueError("ld() needs Rn or [Rn]")


def st(arg):
    """ST Rn or ST @Rn (indirect)"""
    if _is_reg(arg):
        _emit_byte(0x30 | arg)
    elif isinstance(arg, list) and _is_reg(arg[0]):
        _emit_byte(0x50 | arg[0])
    else:
        raise ValueError("st() needs Rn or [Rn]")


def ldd(arg):
    """LDD @Rn: load double-byte indirect"""
    if isinstance(arg, list) and _is_reg(arg[0]):
        _emit_byte(0x60 | arg[0])
    else:
        raise ValueError("ldd() needs [Rn]")


def std(arg):
    """STD @Rn: store double-byte indirect"""
    if isinstance(arg, list) and _is_reg(arg[0]):
        _emit_byte(0x70 | arg[0])
    else:
        raise ValueError("std() needs [Rn]")


def pop(arg):
    """POP @Rn: pop 16-bit via pointer"""
    if isinstance(arg, list) and _is_reg(arg[0]):
        _emit_byte(0x80 | arg[0])
    else:
        raise ValueError("pop() needs [Rn]")


def stp(arg):
    """STP @Rn: store-pop 16-bit via pointer"""
    if isinstance(arg, list) and _is_reg(arg[0]):
        _emit_byte(0x90 | arg[0])
    else:
        raise ValueError("stp() needs [Rn]")


def add(r):
    """ADD Rn: add register to accumulator"""
    if not _is_reg(r):
        raise ValueError(f"Bad register: {r}")
    _emit_byte(0xA0 | r)


def sub(r):
    """SUB Rn: subtract register from accumulator"""
    if not _is_reg(r):
        raise ValueError(f"Bad register: {r}")
    _emit_byte(0xB0 | r)


def popd(arg):
    """POPD @Rn: pop double-byte indirect"""
    if isinstance(arg, list) and _is_reg(arg[0]):
        _emit_byte(0xC0 | arg[0])
    else:
        raise ValueError("popd() needs [Rn]")


def cpr(r):
    """CPR Rn: compare register to accumulator"""
    if not _is_reg(r):
        raise ValueError(f"Bad register: {r}")
    _emit_byte(0xD0 | r)


def inr(r):
    """INR Rn: increment register"""
    if not _is_reg(r):
        raise ValueError(f"Bad register: {r}")
    _emit_byte(0xE0 | r)


def dcr(r):
    """DCR Rn: decrement register"""
    if not _is_reg(r):
        raise ValueError(f"Bad register: {r}")
    _emit_byte(0xF0 | r)


def br(lbl):
    _fixup_branch(0x01, lbl)


def bnc(lbl):
    _fixup_branch(0x02, lbl)


def bc(lbl):
    _fixup_branch(0x03, lbl)


def bp(lbl):
    _fixup_branch(0x04, lbl)


def bm(lbl):
    _fixup_branch(0x05, lbl)


def bz(lbl):
    _fixup_branch(0x06, lbl)


def bnz(lbl):
    _fixup_branch(0x07, lbl)


def bm1(lbl):
    _fixup_branch(0x08, lbl)


def bnm1(lbl):
    _fixup_branch(0x09, lbl)


def bk():
    _emit_byte(0x0A)


def rs():
    _emit_byte(0x0B)


def bs(lbl):
    _fixup_branch(0x0C, lbl)


# fmt: off
RTN, SET, LD, ST, LDD, STD, POP, STP, ADD, SUB, POPD, CPR, INR, DCR, BR, BNC, BC, BP, BM, BZ, BNZ, BM1, BNM1, BK, RS, BS = rtn, setr, ld, st, ldd, std, pop, stp, add, sub, popd, cpr, inr, dcr, br, bnc, bc, bp, bm, bz, bnz, bm1, bnm1, bk, rs, bs
