# amaranth: UnusedElaboratable=no

from amaranth import Signal, Module, Elaboratable, ClockSignal, ResetSignal, Array
from amaranth.sim import Simulator
from amaranth.asserts import Assert, Assume, Past, Rose, Initial

from register import Register


class RegisterFile(Elaboratable):
    def __init__(self, width, depth):
        self.width = width
        self.depth = depth

        self.addr = Signal(range(self.depth))
        self.dout = Signal(width)
        self.din = Signal(width)
        self.load = Signal()

        self.registers = Array()
        for i in range(self.depth):
            self.registers.append(Register(width=self.width))

    def elaborate(self, platform):
        m = Module()

        m.d.comb += self.dout.eq(self.registers[self.addr].d)

        with m.If(self.load):
            m.d.sync += self.registers[self.addr].d.eq(self.din)

        return m

    def ports(self):
        return [self.addr, self.dout, self.din, self.load]

    @classmethod
    def simulate(cls):
        m = Module()
        m.submodules.rf = rf = cls(width=32, depth=32)

        sim = Simulator(m)
        sim.add_clock(1e-6)

        def process():
            yield rf.load.eq(0)
            yield rf.din.eq(0xDEADBEEF)
            for i in range(rf.depth):
                yield rf.addr.eq(i)
                yield

            yield rf.load.eq(1)
            for i in range(rf.depth):
                yield rf.addr.eq(i)
                yield

            yield rf.load.eq(0)
            yield rf.din.eq(0xBEEFDEAD)
            for i in range(rf.depth):
                yield rf.addr.eq(i)
                yield

        sim.add_sync_process(process)
        with sim.write_vcd("register_file.vcd", "register_file.gtkw", traces=rf.ports()):
            sim.run()

    @classmethod
    def formal(cls):
        m = Module()
        m.submodules.rf = rf = cls(width=32, depth=32)
        registers = rf.registers

        clock = ClockSignal("sync")
        reset = ResetSignal("sync")

        m.d.comb += Assume(clock == ~Past(clock))
        m.d.comb += Assume(~reset)

        m.d.comb += Assert(registers[rf.addr].q == rf.dout)

        with m.If(Rose(clock) & ~Initial()):
            with m.If(rf.load):
                m.d.comb += Assert(registers[rf.addr].q == Past(rf.din))

        return m, rf.ports()


if __name__ == "__main__":
    RegisterFile.simulate()
