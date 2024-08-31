import collections
import string
import sys
import typing
# import pyparsing - available if you need it!
# import lark - available if you need it!
NUMBERS = string.digits
ALPHANUMERIC = string.ascii_letters + NUMBERS + "_"
def tokenize_regex(pattern: str) -> typing.List[str]:
    tokens = []
    i = 0
    if pattern[0] == "^":  # Start of Anchor
        tokens.append(pattern)
        i += len(pattern)
    if pattern[-1] == "$":  # End of Anchor
        tokens.append(pattern)
        i += len(pattern)
    while i < len(pattern):
        if pattern[i] == "\\":
            tokens.append(pattern[i : i + 2])
            i += 2
        elif pattern[i] == "[":
            end_index = i + 1
            while pattern[end_index] != "]":
                end_index += 1
            tokens.append(pattern[i : end_index + 1])
            i = end_index + 1
        else:
            tokens.append(pattern[i])
            i += 1
    return tokens
def match_pattern(input_line: str, pattern_list: typing.List[str]) -> bool:
    if len(input_line) == 0 and len(pattern_list) == 0:
        return True
    if len(pattern_list) == 0:
        return True
    if not input_line:
        return False
    if pattern_list[0][0] == "^":
        return input_line.startswith(pattern_list[0][1:])
    if pattern_list[0][-1] == "$":
        return input_line.endswith(pattern_list[0][:-1])
    if pattern_list[0] == input_line[0]:
        return match_pattern(input_line[1:], pattern_list[1:])
    elif pattern_list[0] == "\\d":
        for i in range(len(input_line)):
            if input_line[i].isdigit():
                return match_pattern(input_line[i + 1 :], pattern_list[1:])
        else:
            return False
    elif pattern_list[0] == "\\w":
        for i in range(len(input_line)):
            if input_line[i].isalnum():
                return match_pattern(input_line[i + 1 :], pattern_list[1:])
        else:
            return False
    elif pattern_list[0][0] == "[" and pattern_list[0][-1] == "]":
        if pattern_list[0][1] == "^":
            for i in range(len(input_line)):
                if input_line[i] not in pattern_list[0][2:-1]:
                    return match_pattern(input_line[i + 1 :], pattern_list[1:])
            else:
                return False
        else:
            for i in range(len(input_line)):
                if input_line[i] in pattern_list[0][1:-1]:
                    return match_pattern(input_line[i + 1 :], pattern_list[1:])
            else:
                return False
    return match_pattern(input_line[1:], pattern_list)
def main():
    pattern = sys.argv[2]
    input_line = sys.stdin.read()
    if sys.argv[1] != "-E":
        print("Expected first argument to be '-E'")
        exit(1)
    pattern_list = tokenize_regex(pattern)
    if match_pattern(input_line, pattern_list):
        exit(0)
    else:
        exit(1)
if __name__ == "__main__":
    main()