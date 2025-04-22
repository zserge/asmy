class Assembler:
    def __init__(self, endian="little", pc_start=0):
        self.rom = bytearray()
        self.pc_start = pc_start
        self.pc = pc_start
        self.labels = {}
        self.fixups = []
        self.endian = endian

    def reset(self):
        self.rom.clear()
        self.pc = self.pc_start
        self.labels.clear()
        self.fixups.clear()

    class Label:
        def __init__(self, name, assembler):
            self.name = name
            self.assembler = assembler

        def __enter__(self):
            # TODO: fail on duplicate labels
            self.assembler.labels[self.name] = self.assembler.pc
            self.assembler._resolve_fixups(self.name)
            return self

        def __exit__(self, *args):
            pass

        def addr(self):
            if not self.name in self.assembler.labels:
                raise ValueError(f"Label {self.name} not defined")
            return self.assembler.labels[self.name]

    def _resolve_fixups(self, label_name):
        if label_name not in self.labels:
            return
        address = self.labels[label_name]
        remaining = []
        for fixup in self.fixups:
            pos, lname, patch_fn = fixup
            if lname == label_name:
                try:
                    patch_fn(self.rom, pos, address)
                except Exception as e:
                    raise ValueError(f"Error patching {label_name} at {pos:04x}: {e}")
            else:
                remaining.append(fixup)
        self.fixups = remaining

    def _emit_label_ref(self, label, size):
        def resolver(rom, pos, address):
            resolved = address
            rom[pos : pos + size] = resolved.to_bytes(size, self.endian)

        if label.name in self.labels:
            resolver(self.rom, len(self.rom), self.labels[label.name])
        else:
            pos = len(self.rom)
            self.rom += bytes(size)
            self.pc += size
            self.fixups.append((pos, label.name, resolver))

    def fixup(self, label, size, patcher):
        pos = len(self.rom)
        self.rom += bytes(size)
        self.pc += size
        if label in self.labels:
            addr = self.labels[label]
            patcher(self.rom, pos, addr)
        else:
            self.fixups.append((pos, label, patcher))

    def label(self, name):
        return self.Label(name, self)

    def org(self, address):
        if address < len(self.rom) + self.pc_start:
            raise ValueError(f"ORG conflict at {address:04X}")
        self.rom += bytes(address - self.pc_start - len(self.rom))
        self.pc = address

    def db(self, *values):
        for v in values:
            if isinstance(v, str):
                self.rom += v.encode("ascii")
                self.pc += len(v)
            elif isinstance(v, self.Label):
                self._emit_label_ref(v, 1)
            else:
                self.rom.append(v & 0xFF)
                self.pc += 1

    def dw(self, *values):
        for v in values:
            if isinstance(v, self.Label):
                self._emit_label_ref(v, 2)
            else:
                self.rom += (v & 0xFFFF).to_bytes(2, self.endian)
                self.pc += 2

    def finalize(self):
        if self.fixups:
            unresolved = [
                f"Unresolved reference {label} at {pos:04X}"
                for pos, label, _ in self.fixups
            ]
            raise ValueError("\n".join(unresolved))
        return bytes(self.rom)
