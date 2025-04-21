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
pip install asmy
```
