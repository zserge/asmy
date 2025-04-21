from asmy.chip8 import L, JP, CLS, org, asm

org(0x200)
with L('start'):
    CLS()
    JP(L('start'))

try:
    rom = asm.finalize()
    print(f"CHIP-8 ROM ({len(rom)} bytes):")
    print(rom.hex(' '))
except ValueError as e:
    print("Error:", e)
