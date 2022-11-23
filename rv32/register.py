# amaranth: UnusedElaboratable=no

from amaranth import Signal, Module, Elaboratable, ClockSignal, ResetSignal
from amaranth.sim import Simulator
from amaranth.asserts import Assert, Stable, Assume, Past, Rose, Initial


class Register(Elaboratable):
    def __init__(self, width):
        self.width = width

        self.din = Signal(width)
        self.dout = Signal(width)
        self.load = Signal()

    def elaborate(self, platform):
        m = Module()

        with m.If(self.load):
            m.d.sync += self.dout.eq(self.din)

        return m

    def ports(self):
        return [self.dout, self.din, self.load]

    @classmethod
    def simulate(cls):
        m = Module()
        m.submodules.reg = reg = cls(width=32)

        sim = Simulator(m)
        sim.add_clock(1e-6)

        def process():
            yield reg.load.eq(0)
            for i in range(10):
                yield reg.d.eq(i)
                yield
            yield reg.load.eq(1)
            for i in range(10):
                yield reg.d.eq(i)
                yield

    @classmethod
    def formal(cls):
        m = Module()
        m.submodules.reg = reg = cls(width=32)

        clock = ClockSignal("sync")
        reset = ResetSignal("sync")

        m.d.comb += Assume(clock == ~Past(clock))
        m.d.comb += Assume(~reset)

        with m.If(Rose(clock) & ~Initial()):
            with m.If(reg.load):
                m.d.comb += Assert(reg.q == Past(reg.d))
            with m.Else():
                m.d.comb += Assert(Stable(reg.q))

        return m, reg.ports() + [clock, reset]
