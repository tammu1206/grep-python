import sys
# import pyparsing
# import lark - available if you need it!
def match_local(input_line: str, pattern: str):
    if len(pattern) == 0:
        return True
    elif pattern.startswith("\d"):
        return input_line[0].isdigit() and match_local(input_line[1:], pattern[2:])
    elif pattern.startswith("\w"):
        return input_line[0].isalnum() and match_local(input_line[1:], pattern[2:])
    elif pattern.startswith("[^") and "]" in pattern:
        chars = pattern[1 : pattern.index("]")]
        return input_line[0] not in chars and match_local(
            input_line[1:], pattern[pattern.index("]") + 1 :]
        )
    elif pattern.startswith("[") and "]" in pattern:
        chars = pattern[1 : pattern.index("]")]
        return input_line[0] in chars and match_local(
            input_line[1:], pattern[pattern.index("]") + 1 :]
        )
    elif pattern[0] == input_line[0]:
        return match_local(input_line[1:], pattern[1:])
    else:
        return False
def match_pattern(input_line: str, pattern: str):
    if pattern[0] == "^":
        return match_local(input_line, pattern[1:])
    if match_local(input_line, pattern):
        return True
    else:
        truncated = input_line[1:]
        if len(truncated) == 0 or (len(truncated) == 1 and truncated[0] == "\n"):
            return False
        return match_pattern(truncated, pattern)
def main():
    pattern = sys.argv[2]
    input_line = sys.stdin.read()
    if sys.argv[1] != "-E":
        print("Expected first argument to be '-E'")
        exit(1)
    if match_pattern(input_line, pattern):
        exit(0)
    else:
        exit(1)
if __name__ == "__main__":
    main()