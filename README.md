# Asmy - Python Multi-Architecture Assembler

A minimal Python-based assembler for multiple architectures.

## Features

- Pythonic syntax for assembly
- Label support with fixups
- Little/big-endian aware
- ROM generation with .org/.db/.dw

## Example (CHIP-8)

```python
from asmy.chip8 import L, JP, CLS, db, org

org(0x200)
with L('start'):
    CLS()
    JP(L('start'))

db(0x80, 'Hello', 0)
print(asm.finalize().hex())
```

## Installation

```bash
pip install pyasm
```
