from lib.controller import controller
from lib.io.arg_parse import Argument

def main():
    args=Argument()
    control=controller(args=args)
    control.output.print_banner()
    control.start()


if __name__ == '__main__':
    main()
