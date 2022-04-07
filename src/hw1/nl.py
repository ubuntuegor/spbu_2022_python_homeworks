import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="File to read.")
    args = parser.parse_args()

    with open(args.file) as f:
        i = 0
        for line in f:
            c = ""
            if line != "\n":
                i += 1
                c = str(i)
            print(f"{c.rjust(6)}\t{line}", end="")


if __name__ == "__main__":
    main()
