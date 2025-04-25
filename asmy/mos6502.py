from .assembler import Assembler

asm = Assembler(endian="little", pc_start=0)
label = lambda name: asm.label(name)


class Immediate:
    def __init__(self, value=0):
        self.value = value

    def __matmul__(self, value):
        self.value = value
        return self


A, X, Y, I = "A", "X", "Y", Immediate()


def _emit_address(operand, size):
    def patch(rom, pos, addr):
        rom[pos : pos + size] = addr.to_bytes(size, "little")

    if isinstance(operand, int):
        asm.db(operand) if size == 1 else asm.dw(operand)
    else:
        asm.fixup(operand, size, patch)


def _emit(opcodes, arg, index):
    mode, operand = _resolve_mode(opcodes, arg, index)
    try:
        opcode = opcodes[mode]
    except KeyError:
        raise ValueError(f"Invalid addressing mode {mode} for instruction")
    asm.db(opcode)
    if mode == "acc":
        return
    elif mode == "rel":
        if isinstance(operand, int):
            asm.db(operand)
        elif isinstance(operand, str):

            def patch_relative(rom, pos, addr):
                rom[pos] = (addr - (pos + 1)) & 0xFF

            asm.fixup(operand, 1, patch_relative)
    elif mode in ("ind", "inx", "iny"):
        if mode == "ind":
            _emit_address(operand, 2)
        elif mode == "inx":
            _emit_address(operand, 1)
        elif mode == "iny":
            _emit_address(operand, 1)
    elif mode in ("zpg", "zpx", "zpy"):
        _emit_address(operand, 1)
    elif mode in ("abs", "abx", "aby"):
        _emit_address(operand, 2)
    elif mode == "imm":
        asm.db(operand)
    else:
        raise ValueError(f"Unhandled addressing mode {mode}")


def _resolve_mode(opcodes, arg, index):
    if isinstance(arg, Immediate):
        return "imm", arg.value
    if arg == A:
        if "acc" not in opcodes:
            raise ValueError("Accumulator mode not supported")
        if index is not None:
            raise ValueError("Accumulator mode does not support indexing")
        return "acc", None
    if isinstance(arg, list):
        if len(arg) < 1:
            raise ValueError("Invalid indirect argument: empty list")
        if not isinstance(arg[0], (int, str)):
            raise ValueError(f"Invalid indirect argument: {arg}")
        if len(arg) == 1:  # ([a]) or ([a], Y)
            if index is not None and index != Y:
                raise ValueError(f"Invalid index for indirect addressing: {index}")
            return "ind" if index is None else "iny", arg[0]
        if len(arg) == 2 and arg[1] == X:  # ([a, X])
            return "inx", arg[0]
        raise ValueError(f"Invalid indirect argument: {arg}")
    if "rel" in opcodes:
        if not isinstance(arg, (int, str)):
            raise ValueError(f"Invalid relative argument: {arg}")
        return "rel", arg
    zp = isinstance(arg, int) and 0 <= arg < 0x100
    if index == X:
        return "zpx" if zp else "abx", arg
    if index == Y:
        return "zpy" if zp else "aby", arg
    return "zpg" if zp and "zpg" in opcodes else "abs", arg


def _handle_relative(label):
    asm = Assembler.get_current()
    pos = len(asm.rom)
    asm.db(0)  # Placeholder for offset

    def patch(rom, _, addr):
        offset = (addr - (pos + 2)) & 0xFF  # +2 for opcode + offset
        rom[pos] = offset

    asm.fixups.append((pos, label, patch))


# def _emit(op, arg, index):
#     zeropage = lambda: "zpg" in op or "zpx" in op or "zpy" in op
#
#     def patch_abs(rom, pos, addr):
#         rom[pos : pos + 2] = addr.to_bytes(2, "little")
#
#     def patch_rel(rom, pos, addr):
#         rom[pos] = addr & 0xFF
#
#     assert index is None or index == X or index == Y
#     if arg == A:
#         assert index is None
#         asm.db(op["acc"])
#     elif isinstance(arg, Immediate):
#         assert index is None
#         asm.db(op["imm"], arg.value)
#     elif "rel" in op:  # relative
#         assert index is None
#         pass
#     elif isinstance(arg, list):  # indirect: f([a]), f([a,X]) or f([a],Y)
#         if index is None:
#             if len(arg) == 1:
#                 b = op["ind"]
#             else:
#                 assert len(arg) == 2 and arg[1] == X
#                 b = op["inx"]
#         elif index == Y:
#             assert len(arg) == 1
#             b = op["iny"]
#         n = arg[0]
#         if isinstance(n, int):
#             asm.db(b, n & 0xFF)
#         elif isinstance(n, str):
#             # TODO
#             pass
#         else:
#             raise ValueError(f"invalid indirection argument: {arg},{index}")
#     elif isinstance(arg, int) and zeropage() and arg >= 0 and arg < 0x100:  # zero page
#         b = op["zpg"] if index is None else op["zpx"] if index == X else op["zpy"]
#         asm.db(b, arg)
#     elif isinstance(arg, int) and arg > 0xFF and arg < 0x10000:  # absolute
#         b = op["abs"] if index is None else op["abx"] if index == X else op["aby"]
#         asm.db(b, arg & 0xFF, (arg >> 8) & 0xFF)
#


def ADC(arg, index=None):
    """Add with Carry"""
    _emit(
        {
            "imm": 0x69,
            "zpg": 0x65,
            "zpx": 0x75,
            "abs": 0x6D,
            "abx": 0x7D,
            "aby": 0x79,
            "inx": 0x61,
            "iny": 0x71,
        },
        arg,
        index,
    )


def AND(arg, index=None):
    """Logical AND"""
    _emit(
        {
            "imm": 0x29,
            "zpg": 0x25,
            "zpx": 0x35,
            "abs": 0x2D,
            "abx": 0x3D,
            "aby": 0x39,
            "inx": 0x21,
            "iny": 0x31,
        },
        arg,
        index,
    )


def ASL(arg, index=None):
    """Arithmetic Shift Left"""
    _emit({"acc": 0x0A, "zpg": 0x06, "zpx": 0x16, "abs": 0x0E, "abx": 0x1E}, arg, index)


def BCC(arg):
    """Branch if Carry Clear"""
    _emit({"rel": 0x90}, arg, None)


def BCS(arg):
    """Branch if Carry Set"""
    _emit({"rel": 0xB0}, arg, None)


def BEQ(arg):
    """Branch if Equal"""
    _emit({"rel": 0xF0}, arg, None)


def BIT(arg):
    """Bit Test"""
    _emit({"zpg": 0x24, "abs": 0x2C}, arg, None)


def BMI(arg):
    """Branch if Minus"""
    _emit({"rel": 0x30}, arg, None)


def BNE(arg):
    """Branch if Not Equal"""
    _emit({"rel": 0xD0}, arg, None)


def BPL(arg):
    """Branch if Positive"""
    _emit({"rel": 0x10}, arg, None)


def BRK():
    """Force Interrupt"""
    asm.db(0x00)


def BVC(arg):
    """Branch if Overflow Clear"""
    _emit({"rel": 0x50}, arg, None)


def BVS(arg):
    """Branch if Overflow Set"""
    _emit({"rel": 0x70}, arg, None)


def CLC():
    """Clear Carry Flag"""
    asm.db(0x18)


def CLD():
    """Clear Decimal Mode"""
    asm.db(0xD8)


def CLI():
    """Clear Interrupt Disable"""
    asm.db(0x58)


def CLV():
    """Clear Overflow Flag"""
    asm.db(0xB8)


def CMP(arg, index=None):
    """Compare"""
    _emit(
        {
            "imm": 0xC9,
            "zpg": 0xC5,
            "zpx": 0xD5,
            "abs": 0xCD,
            "abx": 0xDD,
            "aby": 0xD9,
            "inx": 0xC1,
            "iny": 0xD1,
        },
        arg,
        index,
    )


def CPX(arg):
    """Compare X Register"""
    _emit({"imm": 0xE0, "zpg": 0xE4, "abs": 0xEC}, arg, None)


def CPY(arg):
    """Compare Y Register"""
    _emit({"imm": 0xC0, "zpg": 0xC4, "abs": 0xCC}, arg, None)


def DEC(arg, index=None):
    """Decrement Memory"""
    _emit({"zpg": 0xC6, "zpx": 0xD6, "abs": 0xCE, "abx": 0xDE}, arg, index)


def DEX():
    """Decrement X Register"""
    asm.db(0xCA)


def DEY():
    """Decrement Y Register"""
    asm.db(0x88)


def EOR(arg, index=None):
    """Exclusive OR"""
    _emit(
        {
            "imm": 0x49,
            "zpg": 0x45,
            "zpx": 0x55,
            "abs": 0x4D,
            "abx": 0x5D,
            "aby": 0x59,
            "inx": 0x41,
            "iny": 0x51,
        },
        arg,
        index,
    )


def INC(arg, index=None):
    """Increment Memory"""
    _emit({"zpg": 0xE6, "zpx": 0xF6, "abs": 0xEE, "abx": 0xFE}, arg, index)


def INX():
    """Increment X Register"""
    asm.db(0xE8)


def INY():
    """Increment Y Register"""
    asm.db(0xC8)


def JMP(arg):
    """Jump"""
    _emit({"abs": 0x4C, "ind": 0x6C}, arg, None)


def JSR(arg):
    """Jump to Subroutine"""
    _emit({"abs": 0x20}, arg, None)


def LDA(arg, index=None):
    """Load Accumulator"""
    _emit(
        {
            "imm": 0xA9,
            "zpg": 0xA5,
            "zpx": 0xB5,
            "abs": 0xAD,
            "abx": 0xBD,
            "aby": 0xB9,
            "inx": 0xA1,
            "iny": 0xB1,
        },
        arg,
        index,
    )


def LDX(arg, index=None):
    """Load X Register"""
    _emit({"imm": 0xA2, "zpg": 0xA6, "zpy": 0xB6, "abs": 0xAE, "aby": 0xBE}, arg, index)


def LDY(arg, index=None):
    """Load Y Register"""
    _emit({"imm": 0xA0, "zpg": 0xA4, "zpx": 0xB4, "abs": 0xAC, "abx": 0xBC}, arg, index)


def LSR(arg, index=None):
    """Logical Shift Right"""
    _emit({"acc": 0x4A, "zpg": 0x46, "zpx": 0x56, "abs": 0x4E, "abx": 0x5E}, arg, index)


def NOP():
    """No Operation"""
    asm.db(0xEA)


def ORA(arg, index=None):
    """Logical Inclusive OR"""
    _emit(
        {
            "imm": 0x09,
            "zpg": 0x05,
            "zpx": 0x15,
            "abs": 0x0D,
            "abx": 0x1D,
            "aby": 0x19,
            "inx": 0x01,
            "iny": 0x11,
        },
        arg,
        index,
    )


def PHA():
    """Push Accumulator"""
    asm.db(0x48)


def PHP():
    """Push Processor Status"""
    asm.db(0x08)


def PLA():
    """Pull Accumulator"""
    asm.db(0x68)


def PLP():
    """Pull Processor Status"""
    asm.db(0x28)


def ROL(arg, index=None):
    """Rotate Left"""
    _emit({"acc": 0x2A, "zpg": 0x26, "zpx": 0x36, "abs": 0x2E, "abx": 0x3E}, arg, index)


def ROR(arg, index=None):
    """Rotate Right"""
    _emit({"acc": 0x6A, "zpg": 0x66, "zpx": 0x76, "abs": 0x6E, "abx": 0x7E}, arg, index)


def RTI():
    """Return from Interrupt"""
    asm.db(0x40)


def RTS():
    """Return from Subroutine"""
    asm.db(0x60)


def SBC(arg, index=None):
    """Subtract with Carry"""
    _emit(
        {
            "imm": 0xE9,
            "zpg": 0xE5,
            "zpx": 0xF5,
            "abs": 0xED,
            "abx": 0xFD,
            "aby": 0xF9,
            "inx": 0xE1,
            "iny": 0xF1,
        },
        arg,
        index,
    )


def SEC():
    """Set Carry Flag"""
    asm.db(0x38)


def SED():
    """Set Decimal Flag"""
    asm.db(0xF8)


def SEI():
    """Set Interrupt Disable"""
    asm.db(0x78)


def STA(arg, index=None):
    """Store Accumulator"""
    _emit(
        {
            "zpg": 0x85,
            "zpx": 0x95,
            "abs": 0x8D,
            "abx": 0x9D,
            "aby": 0x99,
            "inx": 0x81,
            "iny": 0x91,
        },
        arg,
        index,
    )


def STX(arg, index=None):
    """Store X Register"""
    _emit({"zpg": 0x86, "zpy": 0x96, "abs": 0x8E}, arg, index)


def STY(arg, index=None):
    """Store Y Register"""
    _emit({"zpg": 0x84, "zpx": 0x94, "abs": 0x8C}, arg, index)


def TAX():
    """Transfer Accumulator to X"""
    asm.db(0xAA)


def TAY():
    """Transfer Accumulator to Y"""
    asm.db(0xA8)


def TSX():
    """Transfer Stack Pointer to X"""
    asm.db(0xBA)


def TXA():
    """Transfer X to Accumulator"""
    asm.db(0x8A)


def TXS():
    """Transfer X to Stack Pointer"""
    asm.db(0x9A)


def TYA():
    """Transfer Y to Accumulator"""
    asm.db(0x98)
