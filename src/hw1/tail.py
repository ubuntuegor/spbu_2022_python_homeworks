import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", dest="lines", type=int, default=10, help="Number of displayed lines.")
    parser.add_argument("file", help="File to read.")
    args = parser.parse_args()

    with open(args.file) as f:
        lines = f.readlines()
        if args.lines > len(lines):
            print(*lines, sep="", end="")
        else:
            print(*lines[-args.lines :], sep="", end="")


if __name__ == "__main__":
    main()
