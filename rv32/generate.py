from amaranth.back import verilog

from program_counter import ProgramCounter

pc = ProgramCounter(width=32, delta=4, reset=0x0)
with open("/tmp/pc.v", "w") as f:
    f.write(verilog.convert(pc, ports=pc.ports()))
