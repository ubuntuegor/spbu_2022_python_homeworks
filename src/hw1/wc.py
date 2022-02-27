import argparse


def count_newlines(data: str) -> int:
    return data.count("\n")


def count_bytes(data: str) -> int:
    return len(data)


def count_words(data: str) -> int:
    return len(data.split())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", dest="newlines", action="store_true", help="Count newlines.")
    parser.add_argument("-w", dest="words", action="store_true", help="Count words.")
    parser.add_argument("-c", dest="bytes", action="store_true", help="Count bytes.")
    parser.add_argument("file", help="File to read.")
    args = parser.parse_args()
    print_all = not args.newlines and not args.words and not args.bytes

    with open(args.file, "r") as f:
        data = f.read()
        if print_all or args.newlines:
            print(count_newlines(data), end=" ")
        if print_all or args.words:
            print(count_words(data), end=" ")
        if print_all or args.bytes:
            print(count_bytes(data), end=" ")
        print()


if __name__ == "__main__":
    main()
