from .assembler import Assembler

asm = Assembler(endian="big", pc_start=0)
label = lambda name: asm.label(name)
org = lambda addr: asm.org(addr * 2)


def _mailbox(op, addr):
    if isinstance(addr, int):
        asm.dw(op * 100 + addr % 100)
    elif isinstance(addr, str):

        def patch(rom, pos, addr_):
            val = (
                op * 100 + (addr_ % 100) // 2
            )  # resolved address is in bytes, not in words
            rom[pos : pos + 2] = val.to_bytes(2, "big")

        asm.fixup(addr, 2, patch)
    else:
        raise ValueError(f"Invalid address type: {addr}")


def lda(x):
    """Load the contents of the given mailbox onto the accumulator."""
    _mailbox(5, x)


def sta(x):
    """Store the contents of the accumulator to the mailbox of the given address."""
    _mailbox(3, x)


def add(x):
    """Add the contents of the given mailbox onto the accumulator."""
    _mailbox(1, x)


def sub(x):
    """Subtract the contents of the given mailbox from the accumulator."""
    _mailbox(2, x)


def inp():
    """Copy the value from the "in box" onto the accumulator"""
    asm.dw(901)


def out():
    """Copy the value from the accumulator to the "out box"."""
    asm.dw(902)


def hlt():
    """Causes the Little Man Computer to stop executing your program."""
    asm.dw(0)


def brz(x):
    """If the contents of the accumulator are 000, the PC will be set to the given address"""
    _mailbox(7, x)


def brp(x):
    """If the contents of the accumulator are 000 or positive, the PC will be set to the given address."""
    _mailbox(8, x)


def bra(x):
    """Set the PC to the given address."""
    _mailbox(6, x)


def dat(x=0):
    """Reseve mailbox for data storage."""
    _mailbox(0, x)


def mem():
    """Return the current memory as a list of numbers 0..999."""
    rom = asm.rom
    assert len(rom) % 2 == 0
    return [int.from_bytes(rom[i : i + 2], "big") for i in range(0, len(rom), 2)]


# fmt: off
LDA, STA, ADD, SUB, INP, OUT, HLT, BRZ, BRP, BRA, DAT = lda, sta, add, sub, inp, out, hlt, brz, brp, bra, dat
