import sys
def match_digit(char: str):
    return ord("0") <= ord(char) <= ord("9")
def match_alphabets(char: str):
    is_upper = ord("A") <= ord(char) <= ord("Z")
    is_lower = ord("a") <= ord(char) <= ord("z")
    return is_upper or is_lower
def match_alphanum(char: str):
    return match_alphabets(char) or match_digit(char) or char == "_"
def match_pcg(char: str, group: str):
    return char in group
def match_ncg(char: str, group: str):
    return char not in group
def is_ncgp(pattern):
    return len(pattern) >= 4 and pattern[0:2] == "[^" and pattern[-1] == "]"
def is_pcgp(pattern):
    return len(pattern) >= 3 and pattern[0] == "[" and pattern[-1] == "]"
def is_alphap(pattern):
    return pattern == "\\w"
def is_digitp(pattern):
    return pattern == "\\d"
def match_character(char: str, pattern: str):
    if is_ncgp(pattern):
        return match_ncg(char, pattern)
    if is_pcgp(pattern):
        return match_pcg(char, pattern)
    if is_alphap(pattern):
        return match_alphanum(char)
    if is_digitp(pattern):
        return match_digit(char)
    if pattern == ".":
        return bool(char)
    return pattern == char
def parse(regex: str):
    j = 0
    pattern = []
    while j < len(regex):
        if regex[j : j + 2] == "\\d":
            j += 2
            pattern.append("\\d")
        elif regex[j : j + 2] == "\\w":
            j += 2
            pattern.append("\\w")
        elif regex[j : j + 2] == "[^" and regex.find("]") != -1:
            end = regex.find("]") + 1
            pattern.append(regex[j:end])
            j = end
        elif regex[j : j + 1] == "[" and regex.find("]") != -1:
            end = regex.find("]") + 1
            pattern.append(regex[j:end])
            j = end
        else:
            pattern.append(regex[j])
            j += 1
    return pattern
def match_pattern(text: str, pattern: str):
    regex = parse(pattern)
    if regex and regex[0] == "^":
        return match_here(text, regex[1:])
    while text:
        if match_here(text, regex):
            return True
        text = text[1:]
def match_here(text, regex):
    if not regex:
        return True
    if len(regex) == 1 and regex[0] == "$":
        return not text
    if len(regex) == 1 and len(text) == 1:
        return match_character(text[0], regex[0])
    if len(regex) >= 2 and regex[1] == "+":
        return match_plus(
            regex[0],
            text,
            regex[2:],
        )
    if len(regex) >= 2 and regex[1] == "?":
        return match_star(
            regex[0],
            text,
            regex[2:],
        )
    if len(regex) >= 2 and regex[0] == "(" and ")" in regex:
        end_index = regex.index(")")
        or_patterns = [parse(regex) for regex in "".join(regex[1:end_index]).split("|")]
        after_part = regex[end_index + 1 :]
        for pattern in or_patterns:
            if match_here(text, pattern + after_part):
                return True
        return False
    if text and match_character(text[0], regex[0]):
        return match_here(text[1:], regex[1:])
    return False
def match_plus(char, text, regex):
    if not match_character(text[0], char[0]):
        return False
    while text and match_character(text[0], char[0]):
        text = text[1:]
    return match_here(text, regex)
def match_star(char, text, regex):
    while text and match_character(text[0], char[0]):
        text = text[1:]
    return match_here(text, regex)
def main():
    pattern = sys.argv[2]
    text = sys.stdin.read().rstrip("\n")
    if sys.argv[1] != "-E":
        exit(1)
    if match_pattern(text, pattern):
        exit(0)
    exit(1)

if __name__ == "__main__":
    main()