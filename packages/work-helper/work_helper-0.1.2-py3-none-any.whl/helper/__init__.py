"""helper tool"""
__version__ = "0.1.2"


from typing import TextIO


class EnhancedWriter:
    def __init__(self, writer: TextIO) -> None:
        self.writer = writer

    def write(self, s: str):
        return self.writer.write(s)

    def writeln(self, s: str = "", intent: int = 0):
        if s is not str:
            s = str(s)
        if intent == 0:
            return self.writer.write(s + "\n")
        lines = s.splitlines(keepends=True)
        for line in lines:
            self.writer.write(f"{' '*intent}{line}")
        self.writer.write("\n")
