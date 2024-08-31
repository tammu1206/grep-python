import sys
# import pyparsing - available if you need it!
# import lark - available if you need it!
specialCharactersToValueMap = {}
def get_literals_from_pattern(pattern):
    i = 0
    literals = []
    while i < len(pattern):
        if pattern[i] == "\\":
            literals.append(pattern[i : i + 2])
            i += 2
        elif pattern[i] == "[":
            end_index = pattern.find("]", i)
            literals.append(pattern[i : i + end_index + 1])
            i = end_index + 1
        else:
            literals.append(pattern[i])
            i += 1
    return literals
def get_real_values(literal):
    literal_values = []
    if len(literal) == 1:
        literal_values = [literal]
    elif literal[0] == "[":
        if literal[1] == "^":
            sub_literals = get_literals_from_pattern(literal[2:-1])
            non_literal_values = []
            for x in sub_literals:
                non_literal_values += get_real_values(x)
            non_literal_values = set(non_literal_values)
            literal_values = [
                chr(i) for i in range(256) if chr(i) not in non_literal_values
            ]
        else:
            sub_literals = get_literals_from_pattern(literal[1:-1])
            literal_values = []
            for x in sub_literals:
                literal_values += get_real_values(x)
            literal_values = set(literal_values)
    else:
        literal_values = specialCharactersToValueMap.get(literal, [])
    return literal_values
def recursive_regex_match(input_line, input_idx, pattern, pattern_idx):
    if pattern_idx == len(pattern):
        return True
    if pattern[pattern_idx] == ["$"]:
        return input_idx == len(input_line) and pattern_idx == len(pattern) - 1
    if input_idx == len(input_line):
        return False
    if input_line[input_idx] in pattern[pattern_idx]:
        if len(pattern) != pattern_idx + 1 and pattern[pattern_idx + 1] == ["+"]:
            return recursive_regex_match(
                input_line, input_idx + 1, pattern, pattern_idx
            ) or recursive_regex_match(
                input_line, input_idx + 1, pattern, pattern_idx + 2
            )
        return recursive_regex_match(
            input_line, input_idx + 1, pattern, pattern_idx + 1
        )
    return False
def match_pattern(input_line, pattern):
    pattern_values = [
        get_real_values(literal) for literal in get_literals_from_pattern(pattern)
    ]
    if pattern_values[0] == ["^"]:
        return recursive_regex_match(input_line, 0, pattern_values, 1)
    else:
        for i in range(len(input_line)):
            if recursive_regex_match(input_line, i, pattern_values, 0):
                return True
        return False
    # else:
    #     raise RuntimeError(f"Unhandled pattern: {pattern}")
def main():
    pattern = sys.argv[2]
    input_line = sys.stdin.read()
    specialCharactersToValueMap["\\d"] = [str(i) for i in range(10)]
    specialCharactersToValueMap["\\w"] = [chr(i) for i in range(ord("a"), ord("z") + 1)]
    specialCharactersToValueMap["\\w"] += [
        chr(i) for i in range(ord("A"), ord("Z") + 1)
    ]
    specialCharactersToValueMap["\\w"] += [
        chr(i) for i in range(ord("0"), ord("9") + 1)
    ]
    specialCharactersToValueMap["\\w"] += ["_"]
    specialCharactersToValueMap["\\\\"] = ["\\"]
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