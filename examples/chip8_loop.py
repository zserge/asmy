from asmy.chip8 import *

org(0x200)
with label("start"):
    ld(V0, 0)
with label("loop"):
    add(V0, 1)
    cls()
    jp("loop")

try:
    rom = asm.finalize()
    print(f"CHIP-8 ROM ({len(rom)} bytes):")
    print(rom.hex(" ", 2))
except ValueError as e:
    print("Error:", e)
