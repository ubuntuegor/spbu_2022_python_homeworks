import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="File to read.")
    args = parser.parse_args()

    with open(args.file, "r") as f:
        for i, line in enumerate(f):
            print(f"{i + 1} {line}", end="")


if __name__ == "__main__":
    main()
