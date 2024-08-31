import sys
# import pyparsing - available if you need it!
# import lark - available if you need it!
def matcher(input_line, pattern):
    ptr1 = 0
    ptr2 = 0
    if input_line == "" and pattern == "":
        return True
    elif input_line == "":
        return False
    elif pattern == "":
        return True
    while ptr1 < len(input_line):
        if ptr2 + 1 < len(pattern) and pattern[ptr2 : ptr2 + 2] == "\\d":
            if input_line[ptr1].isdigit():
                return matcher(input_line[ptr1 + 1 :], pattern[ptr2 + 2 :])
            else:
                ptr1 = ptr1 + 1
        elif ptr2 + 1 < len(pattern) and pattern[ptr2 : ptr2 + 2] == "\\w":
            if input_line[ptr1].isalnum():
                return matcher(input_line[ptr1 + 1 :], pattern[ptr2 + 2 :])
            else:
                ptr1 = ptr1 + 1
        elif input_line[ptr1] == pattern[ptr2]:
            return matcher(input_line[ptr1 + 1 :], pattern[ptr2 + 1 :])
        else:
            ptr1 = ptr1 + 1
    return False
def match_pattern(input_line, pattern):
    if len(pattern) == 1:
        return pattern in input_line
    elif pattern == "\\d":
        for i in range(10):
            if input_line.find(str(i)) != -1:
                return True
    elif pattern == "\\w":
        return input_line.isalnum()
    elif pattern[0:2] == "[^":
        pat = pattern[2:-1]
        for ch in pat:
            if input_line.find(ch) != -1:
                return False
        return True
    elif pattern[0] == "[" and pattern[-1] == "]":
        pat = pattern[1:-1]
        for ch in pat:
            if input_line.find(ch) != -1:
                return True
        return False
    else:
        raise RuntimeError(f"Unhandled pattern: {pattern}")
        return matcher(input_line, pattern)
def main():
    pattern = sys.argv[2]
    input_line = sys.stdin.read()
    if sys.argv[1] != "-E":
        print("Expected first argument to be '-E'")
        exit(1)
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")
    # Uncomment this block to pass the first stage
    if match_pattern(input_line, pattern):
        exit(0)
    else:
        exit(1)
if __name__ == "__main__":
    main()