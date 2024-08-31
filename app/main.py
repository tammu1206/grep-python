import sys

# import pyparsing - available if you need it!
# import lark - available if you need it!


def match_pattern(input_line, pattern):
    if len(pattern) == 1:
        # Original single-character pattern match
        return pattern in input_line
    elif pattern == r"\d":
        # Check for any digit in the input line
        return any(char.isdigit() for char in input_line)
    elif pattern == r"\w":
        # Check for any alphanumeric character or underscore in the input line
        return any(char.isalnum() or char == '_' for char in input_line)
    else:
        raise RuntimeError(f"Unhandled pattern: {pattern}")


def main():
    pattern = sys.argv[2]
    input_line = sys.stdin.read()

    if sys.argv[1] != "-E":
        print("Expected first argument to be '-E'")
        exit(1)

    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Check if the input line matches the pattern
    if match_pattern(input_line, pattern):
        exit(0)
    else:
        exit(1)


if __name__ == "__main__":
    main()
