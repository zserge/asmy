class Assembler:
    """A simple assembler for a hypothetical CPU architecture.

    This assembler uses Python syntax for assembly code:
    - Labels are defined using 'with assembler.label("name"):' blocks
    - Label references are used to emit addresses in db/dw instructions
    - Commands are emitted as raw bytes
    """

    def __init__(self, endian="little", pc_start=0):
        """Initialize a new assembler instance.

        Args:
            endian: Byte order for multi-byte values ("little" or "big")
            pc_start: Starting address for the program counter
        """
        self.rom = bytearray()
        self.pc = pc_start
        self.labels = {}
        self.fixups = []
        self.endian = endian

    class Label:
        """A label in the assembler, used for defining and referencing locations in the code.

        Labels can be used in two ways:
        1. Within a 'with' block to define a location: with asm.label("start"): ...
        2. As a value in db/dw to reference a location: asm.dw(asm.label("start"))
        """

        __slots__ = ("name", "assembler", "offset")

        def __init__(self, name, assembler):
            self.name = name
            self.assembler = assembler
            self.offset = 0

        def __enter__(self):
            """Called when entering a 'with' block, defines the label at current PC."""
            self.assembler.labels[self.name] = self.assembler.pc + self.offset
            self.assembler._resolve_fixups(self.name)
            return self

        def __exit__(self, *args):
            pass

        def __add__(self, offset):
            """Support for label + offset operations."""
            new_label = Assembler.Label(self.name, self.assembler)
            new_label.offset = self.offset + offset
            return new_label

        def __sub__(self, offset):
            """Support for label - offset operations."""
            return self.__add__(-offset)

    def _resolve_fixups(self, label_name):
        """Resolve all fixups for the given label name."""
        if label_name not in self.labels:
            return
        addr = self.labels[label_name]
        for i in reversed(range(len(self.fixups))):
            pos, fn = self.fixups[i]
            if fn(label_name, addr):
                del self.fixups[i]

    def label(self, name):
        """Define a label at the current program counter or reference a label."""
        return self.Label(name, self)

    def org(self, address):
        """Set the program counter to a specific address."""
        if address < len(self.rom):
            raise ValueError(f"ORG conflict at {address:04X}")
        self.rom += bytes(address - len(self.rom))
        self.pc = address

    def db(self, *values):
        """Define raw bytes in the ROM.

        Args:
            values: Bytes, strings, or labels to emit
        """
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
        """Define words (2 bytes) in the ROM.

        Args:
            values: Word values or labels to emit
        """
        for v in values:
            if isinstance(v, self.Label):
                self._emit_label_ref(v, 2)
            else:
                self.rom += (v & 0xFFFF).to_bytes(2, self.endian)
                self.pc += 2

    def _emit_label_ref(self, label, size):
        """Emit a reference to a label.

        If the label is already defined, its address is directly emitted.
        Otherwise, a fixup is registered to be resolved later.

        Args:
            label: The label to reference
            size: Size in bytes (1 for db, 2 for dw)
        """

        def resolver(name, addr):
            if name == label.name:
                # When resolving a forward reference, we should use the raw label address
                # The offset should be applied by the caller, not in the resolver
                resolved = addr
                bytes_val = resolved.to_bytes(size, self.endian)
                self.rom[pos : pos + size] = bytes_val
                return True
            return False

        if label.name in self.labels:
            resolved = self.labels[label.name]  # Don't add offset here
            self.rom += resolved.to_bytes(size, self.endian)
        else:
            pos = len(self.rom)
            self.rom += bytes(size)
            self.fixups.append((pos, resolver))
        self.pc += size

    def finalize(self):
        """Finalize the assembly process, checking for unresolved references.

        Returns:
            bytes: The assembled ROM data

        Raises:
            ValueError: If any label references remain unresolved
        """
        if self.fixups:
            unresolved = [
                f"Unresolved reference at {pos:04X}" for pos, _ in self.fixups
            ]
            raise ValueError("\n".join(unresolved))
        return bytes(self.rom)
