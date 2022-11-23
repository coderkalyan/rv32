from amaranth.cli import main_parser, main_runner

from program_counter import ProgramCounter
from register import Register
from register_file import RegisterFile


def main():
    parser = main_parser()
    args = parser.parse_args()

    modules = [RegisterFile]

    for module in modules:
        m, ports = module.formal()

        main_runner(parser, args, m, ports=ports)


if __name__ == "__main__":
    main()
