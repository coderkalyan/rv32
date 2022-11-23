# amaranth: UnusedElaboratable=no

from amaranth import Signal, Module, Elaboratable, ClockSignal, ResetSignal
from amaranth.sim import Simulator
from amaranth.asserts import Assert, Stable, Assume, Past, Rose, Initial


class FetchStage(Elaboratable):
    def __init__(self):
        pass

    def elaborate(self, platform):
        m = Module()

        with m.If(self.load):
            m.d.sync += self.dout.eq(self.din)
