class Assembler:
    def __init__(self, endian='little', pc_start=0x200):
        self.rom = bytearray()
        self.pc = pc_start
        self.labels = {}
        self.fixups = []
        self.endian = endian

    class Label:
        __slots__ = ('name', 'assembler', 'offset')
        def __init__(self, name, assembler):
            self.name = name
            self.assembler = assembler
            self.offset = 0

        def __enter__(self):
            self.assembler.labels[self.name] = self.assembler.pc + self.offset
            self.assembler._resolve_fixups(self.name)
            return self

        def __exit__(self, *args):
            pass

        def __add__(self, offset):
            new_label = Assembler.Label(self.name, self.assembler)
            new_label.offset = self.offset + offset
            return new_label

        def __sub__(self, offset):
            return self.__add__(-offset)

    def _resolve_fixups(self, label_name):
        if label_name not in self.labels:
            return
        addr = self.labels[label_name]
        for i in reversed(range(len(self.fixups))):
            pos, fn = self.fixups[i]
            if fn(label_name, addr):
                del self.fixups[i]

    def org(self, address):
        if address < len(self.rom):
            raise ValueError(f"ORG conflict at {address:04X}")
        self.rom += bytes(address - len(self.rom))
        self.pc = address

    def db(self, *values):
        for v in values:
            if isinstance(v, str):
                self.rom += v.encode('ascii')
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

    def _emit_label_ref(self, label, size):
        def resolver(name, addr):
            if name == label.name:
                resolved = addr + label.offset
                bytes_val = resolved.to_bytes(size, self.endian)
                self.rom[pos:pos+size] = bytes_val
                return True
            return False
        
        if label.name in self.labels:
            resolved = self.labels[label.name] + label.offset
            self.rom += resolved.to_bytes(size, self.endian)
        else:
            pos = len(self.rom)
            self.rom += bytes(size)
            self.fixups.append( (pos, resolver) )
        self.pc += size

    def finalize(self):
        for pos, fn in self.fixups:
            raise ValueError(f"Unresolved reference at {pos:04X}")
        return bytes(self.rom)
