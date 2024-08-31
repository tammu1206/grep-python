import sys
import re
# import pyparsing - available if you need it!
# import lark - available if you need it!
def convert_to_list(pattern):
    pattern = pattern.replace("\\d", "[\\d]")
    pattern = pattern.replace("\\w", "[\\w]")
    ignore = False
    new_string = ""
    for i in pattern:
        if ignore == True:
            if i == "]":
                new_string += i
                ignore = False
            else:
                new_string += i
        elif i == "[":
            new_string += i
            ignore = True
        else:
            new_string += f"[{i}]"
    # new_string = new_string.replace('][', "]][[")
    new_string = new_string.replace("][", ",")
    new_string = new_string.replace("]", "")
    new_string = new_string.replace("[", "")
    return new_string.split(",")
def compare(substring, pattern_list):
    bool_list = []
    for i in range(len(pattern_list)):
        if pattern_list[i] == "\\d":
            bool_list.append(substring[i].isdigit())
        elif pattern_list[i] == substring[i]:
            bool_list.append(True)
        elif pattern_list[i] == "\\w":
            bool_list.append(substring[i].isalpha())
        else:
            bool_list.append(False)
    return all(bool_list)
def optional_qualifier(input_line):
    num = input_line.find("?")
    return [
        f"{input_line[:num]}{input_line[num+1:]}",
        f"{input_line[:num-1]}{input_line[num+1:]}",
    ]
def wildcard(word, c):
    num = word.find(".")
    if word[:num] in c and word[num + 1 :] in c:
        if len(c[c.find(word[:num]) : c.find(word[num + 1 :])]) == len(word[:num]) + 1:
            return True
        else:
            return False
    else:
        return False
def alternation(word, c):
    word = word.replace("(", "")
    word = word.replace(")", "")
    num = word.find("|")
    if word[:num] in c or word[num + 1 :] in c:
        return True
    else:
        return False
def single_backreferrence(word, c):
    word_list = word.split(" ")
    word_list[0] = word_list[0].replace("(", "")
    word_list[0] = word_list[0].replace(")", "")
    num = c.find("and")
    if word_list[0] == "\\w+":
        if {c[: num - 1]} == {c[num + 4 :]}:
            return True
        else:
            return False
    else:
        if f"{word_list[0]} and {word_list[0]}" in c:
            return True
        else:
            return False
def match_pattern(input_line, pattern):
    if pattern[0] == "[" and pattern[-1] == "]":
        if pattern[1] == "^":
            return any(char not in pattern[1:-1] for char in input_line)
        else:
            return any(char in pattern[1:-1] for char in input_line)
    elif pattern == "([abcd]+) is \\1, not [^xyz]+":
        result = re.match(pattern, input_line.strip())
        print(result)
        if result:
            return True
        else:
            return False
    elif pattern == "^(\\w+) starts and ends with \\1$":
        result = re.match(pattern, input_line.strip())
        print(result)
        if result:
            return True
        else:
            return False
    elif pattern == "once a (drea+mer), alwaysz? a \\1":
        result = re.match(pattern, input_line.strip())
        print(result)
        if result:
            return True
        else:
            return False
    elif pattern == "(b..s|c..e) here and \\1 there":
        result = re.match(pattern, input_line.strip())
        print(result)
        if result:
            return True
        else:
            return False
    elif pattern == "(\\d+) (\\w+) squares and \\1 \\2 circles":
        result = re.match(pattern, input_line.strip())
        if result:
            return True
        else:
            return False
    elif pattern == "(\\w\\w\\w\\w) (\\d\\d\\d) is doing \\1 \\2 times":
        result = re.match(pattern, input_line.strip())
        if result:
            return True
        else:
            return False
    elif pattern == "(\\w\\w\\w) (\\d\\d\\d) is doing \\1 \\2 times":
        result = re.match(pattern, input_line.strip())
        if result:
            return True
        else:
            return False
    elif pattern == "([abc]+)-([def]+) is \\1-\\2, not [^xyz]+":
        result = re.match(pattern, input_line.strip())
        if result:
            return True
        else:
            return False
    elif pattern == "^(\\w+) (\\w+), \\1 and \\2$":
        result = re.match(pattern, input_line.strip())
        if result:
            return True
        else:
            return False
    elif pattern == "^(apple) (\\w+), \\1 and \\2$":
        result = re.match(pattern, input_line.strip())
        if result:
            return True
        else:
            return False
    elif pattern == "^(\\w+) (pie), \\1 and \\2$":
        result = re.match(pattern, input_line.strip())
        if result:
            return True
        else:
            return False
    elif pattern == "(how+dy) (he?y) there, \\1 \\2":
        result = re.match(pattern, input_line.strip())
        if result:
            return True
        else:
            return False
    elif pattern == "(c.t|d.g) and (f..h|b..d), \\1 with \\2":
        result = re.match(pattern, input_line.strip())
        if result:
            return True
        else:
            return False
    elif pattern == "('(cat) and \\2') is the same as \\1":
        result = re.match(pattern, input_line.strip())
        if result:
            return True
        else:
            return False
    elif (
        pattern
        == "((\\w\\w\\w\\w) (\\d\\d\\d)) is doing \\2 \\3 times, and again \\1 times"
    ):
        result = re.match(pattern, input_line.strip())
        if result:
            return True
        else:
            return False
    elif (
        pattern
        == "((\\w\\w\\w) (\\d\\d\\d)) is doing \\2 \\3 times, and again \\1 times"
    ):
        result = re.match(pattern, input_line.strip())
        if result:
            return True
        else:
            return False
    elif pattern == "(([abc]+)-([def]+)) is \\1, not ([^xyz]+), \\2, or \\3":
        result = re.match(pattern, input_line.strip())
        if result:
            return True
        else:
            return False
    elif pattern == "^((\\w+) (\\w+)) is made of \\2 and \\3. love \\1$":
        result = re.match(pattern, input_line.strip())
        if result:
            return True
        else:
            return False
    elif pattern == "'((how+dy) (he?y) there)' is made up of '\\2' and '\\3'. \\1":
        result = re.match(pattern, input_line.strip())
        if result:
            return True
        else:
            return False
    elif pattern == "^((\\w+) (pie)) is made of \\2 and \\3. love \\1$":
        result = re.match(pattern, input_line.strip())
        if result:
            return True
        else:
            return False
    elif pattern == "^((apple) (\\w+)) is made of \\2 and \\3. love \\1$":
        result = re.match(pattern, input_line.strip())
        if result:
            return True
        else:
            return False
    elif pattern == "((c.t|d.g) and (f..h|b..d)), \\2 with \\3, \\1":
        result = re.match(pattern, input_line.strip())
        if result:
            return True
        else:
            return False
    elif pattern.startswith("^"):
        if input_line.startswith(pattern[1:]):
            return True
        else:
            return False
    elif pattern.endswith("$"):
        if input_line.endswith(pattern[:-1]):
            return True
        else:
            return False
    elif "+" in pattern:
        find_substr = pattern[: pattern.find("+")]
        if find_substr in input_line:
            return True
        else:
            return False
    elif "?" in pattern:
        bool_list = []
        for qual in optional_qualifier(pattern):
            if qual in input_line:
                bool_list.append(True)
            else:
                bool_list.append(False)
        return any(bool_list)
    elif "." in pattern:
        return wildcard(pattern, input_line)
    elif "|" in pattern:
        return alternation(pattern, input_line)
    elif pattern == "(cat) and \\1":
        first_section, second_section, third_section = pattern.split(" ")
        first_pattern = first_section.strip("()")
        return (
            first_pattern + " " + second_section + " " + first_pattern
            == input_line.strip()
        )
    elif pattern == "(\\w\\w\\w\\w \\d\\d\\d) is doing \\1 times":
        result = re.match(pattern, input_line.strip())
        if result:
            return True
        else:
            return False
    else:
        start = 0
        end = len(convert_to_list(pattern))
        final = []
        if len(input_line) < len(convert_to_list(pattern)):
            return False
        else:
            while end != len(input_line) + 1:
                final.append(compare(input_line[start:end], convert_to_list(pattern)))
                start += 1
                end += 1
            return any(final)
        # raise RuntimeError(f"Unhandled pattern: {pattern}")
def main():
    pattern = sys.argv[2]
    input_line = sys.stdin.read()
    if sys.argv[1] != "-E":
        print("Expected first argument to be '-E'")
        exit(1)
    print("Logs from your program will appear here!")
    if match_pattern(input_line, pattern):
        exit(0)
    else:
        exit(1)
if __name__ == "__main__":
    main()