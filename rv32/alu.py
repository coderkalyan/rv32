from amaranth import Signal, Module, Elaboratable
from amaranth.asserts import Assert


class ArithmeticLogicUnit(Elaboratable):
    """
    An N bit arithmetic and logic unit. Performs addition, subtraction,
    boolean algebra, and logical shift operations on two N bit operands (and a carry bit)
    and outputs the N bit result, along with a carry bit.

    Parameters
    ----------
    N : int
        The bit width of the ALU.

    Attributes
    ----------
    op: Signal(), in
        Selects the operation to be performed
    a : Signal(N), in
        First operand
    b : Signal(N), in
        Second operand
    r : Signal(N), out
        Result
    """
    def __init__(self, n):
        self.n = n

        self.op = Signal(3)

        self.a = Signal(self.n)
        self.b = Signal(self.n)

        self.r = Signal(self.n)
    
    def elaborate(self, platform):
        m = Module()

        with m.Switch(self.op):
            with m.Case(0):
                m.d.comb += self.r.eq(self.a + self.b)
            with m.Case(1):
                m.d.comb += self.r.eq(self.a - self.b)
            with m.Case(2):
                m.d.comb += self.r.eq(self.a & self.b)
            with m.Case(3):
                m.d.comb += self.r.eq(self.a | self.b)
            with m.Case(4):
                m.d.comb += self.r.eq(self.a ^ self.b)
            with m.Case(5):
                m.d.comb += self.r.eq(self.a << self.b)
            with m.Case(6):
                arithmetic_shift = self.a >> self.b
                m.d.comb += self.r.eq(arithmetic_shift[:-self.b])
            with m.Case(7):
                m.d.comb += self.r.eq(self.a >> self.b)

        return m
    
    def formal(self):
        
