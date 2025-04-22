# Asmy - Python Multi-Architecture Assembler

[![PyPI](https://img.shields.io/pypi/v/asmy)](https://pypi.org/project/asmy/)
[![Tests](https://github.com/zserge/asmy/actions/workflows/test.yml/badge.svg)](https://github.com/zserge/asmy/actions)
[![License](https://img.shields.io/github/license/zserge/asmy)](LICENSE)
[![Python](https://img.shields.io/pypi/pyversions/asmy)](https://pypi.org/project/asmy/)

A minimal Python-based assembler for multiple architectures.

## Features

- Pythonic syntax for assembly
- Label support with fixups
- Little/big-endian aware
- ROM generation with .org/.db/.dw

## Example (CHIP-8)

```python
from asmy.chip8 import *

org(0x200)
with label("start"):
    ld(V0, 0)
with label("loop"):
    add(V0, 1)
    cls()
    jp("loop")

# Print resulting ROM in hex
print(asm.finalize().hex(" ", 2))
```

## Installation

```bash
pip install asmy
```
