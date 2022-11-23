from amaranth import Signal, Module, Elaboratable
from amaranth.sim import Simulator
from amaranth.asserts import Assert, Assume, Past


class ProgramCounter(Elaboratable):
    def __init__(self, width, increment, reset):
        self.width = width
        self.increment = increment

        self.dout = Signal(width, reset=reset)
        self.ce = Signal()

        self.din = Signal(width)
        self.load = Signal()

    def elaborate(self, platform):
        m = Module()

        with m.If(self.ce):
            m.d.sync += self.dout.eq((self.dout + self.increment).cast(32))
        with m.Elif(self.load):
            m.d.sync += self.dout.eq(self.din)

        return m

    @classmethod
    def simulate(cls):
        m = Module()
        m.submodules.pc = pc = ProgramCounter(width=32, increment=4, reset=0x00000000)

        sim = Simulator(m)
        sim.add_clock(1e-6)

        def process():
            yield pc.ce.eq(0)
            for _ in range(10):
                yield
                assert (yield pc.q == 0)

            yield pc.ce.eq(1)
            yield
            for i in range(256):
                yield
                yield pc.q

        sim.add_sync_process(process)

        with sim.write_vcd("pc.vcd", "pc.gtkw", traces=pc.ports()):
            sim.run()

    def ports(self):
        return [self.dout, self.ce, self.din, self.load]

    @classmethod
    def formal(cls):
        m = Module()
        m.submodules.pc = pc = ProgramCounter(32, 4, 0x00000000)

        m.d.comb += Assert(pc.q == Past(pc.q) + pc.increment)

        return m, pc.ports()


if __name__ == "__main__":
    ProgramCounter.simulate()
