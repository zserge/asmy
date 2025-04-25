from .assembler import Assembler

asm = Assembler(endian="big", pc_start=0)
label = lambda name: asm.label(name)


class Instr(object):
    def __init__(self, callable):
        self._callable = callable

    def __call__(self):
        print("call")
        return self._callable()

    def __repr__(self):
        print("repr")
        self._callable()
        return ""


def ka():
    asm.db(0)


def ao():
    asm.db(1)


def ch():
    asm.db(2)


def cy():
    asm.db(3)


def am():
    asm.db(4)


def ma():
    asm.db(5)


def mp():
    asm.db(6)  # m+


def mm():
    asm.db(7)  # m-


def cal():
    asm.db(0xE)


def rsto():
    cal(0)


def setr():
    cal(1)


def rstr():
    cal(2)


def cmpl():
    cal(4)


def chng():
    cal(5)


def sift():
    cal(6)


def ends():
    cal(7)


def errs():
    cal(8)


def shts():
    cal(9)


def lons():
    cal(0xA)


def sund():
    cal(0xB)


def timr():
    cal(0xC)


def dspr():
    cal(0xD)


def demm():
    cal(0xE)  # dem-


def demp():
    cal(0xF)  # dem+


def tia(x):
    asm.dw(0x0800 | (x & 15))


def aia(x):
    asm.dw(0x0900 | (x & 15))


def tiy(x):
    asm.dw(0x0A00 | (x & 15))


def aiy(x):
    asm.dw(0x0B00 | (x & 15))


def cia(x):
    asm.dw(0x0C00 | (x & 15))


def ciy(x):
    asm.dw(0x0D00 | (x & 15))


def jump(x):
    asm.db(0x0F)
    if isinstance(x, str):

        def patch(rom, pos, addr):
            print(f"addr {addr:x}")
            rom[pos : pos + 2] = [addr >> 4, addr & 0xF]

        asm.fixup(x, 2, patch)
    elif isinstance(x, int):
        asm.dw(x)
    else:
        raise ValueError(f"Invalid jump address: {x}")


def mem(sep=""):
    return sep.join([f"{(x&15):x}" for x in asm.rom])


# fmt: off
KA, AO, CH, CY, AM, MA, MP, MM, CAL, RSTO, SETR, RSTR, CMPL, CHNG, SIFT, ENDS, ERRS, SHTS, LONS, SUND, TIMR, DSPR, DEMM, DEMP, TIA, AIA, TIY, AIY, CIA, CIY, JUMP = ka, ao, ch, cy, am, ma, mp, mm, cal, rsto, setr, rstr, cmpl, chng, sift, ends, errs, shts, lons, sund, timr, dspr, demm, demp, tia, aia, tiy, aiy, cia, ciy, jump
