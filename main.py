import argps
from engine import engine

if __name__ == '__main__':

    # get a command-line parser.
    p = argps.parser()

    # parse the command-line arguments.
    args = p.parse_args()

    # print the arguments
    print(f"Command-line args: {args}")

    # call the main function
    engine(args).run()