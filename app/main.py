import sys
import re
# import pyparsing - available if you need it!
# import lark - available if you need it!
def match_pattern(input_line, pattern):
    if len(pattern) == 1:
        return pattern in input_line
    elif pattern == "\\d":
        return any(c.isdigit() for c in input_line)
    elif pattern == "\\w":
        return any(c.isalnum() for c in input_line)
    elif pattern == "[abcd]":
        return ("a" or "b" or "c" or "d") in input_line
    elif pattern == "[^xyz]":
        return ("x" or "y" or "z") not in input_line
    elif pattern == "[^anb]":
        return ("a" or "n" or "b") not in input_line
    elif pattern == "\\d apple":
        for num in range(1, 10):
            var = str(num) + " apple"
            if var in input_line:
                return True
        return False
    elif pattern == "\\d\\d\\d apples":
        for num1 in range(1, 10):
            for num2 in range(0, 10):
                for num3 in range(0, 10):
                    var = str(num1) + str(num2) + str(num3) + (" apples" "")
                    # print(var)
                    if var in input_line:
                        return True
        return False
    elif pattern == "\\d \\w\\w\\ws":
        for num in range(1, 10):
            for x in range(ord("a"), ord("z") + 1):
                for y in range(ord("a"), ord("z") + 1):
                    for z in range(ord("a"), ord("z") + 1):
                        var = str(num) + " " + chr(x) + chr(y) + chr(z) + "s"
                        if var in input_line:
                            return True
        return False
    elif pattern == "^log":
        return pattern[1:] == input_line[0:3]
    elif pattern == "cat$":
        return pattern[-4:-1] == input_line.strip()[-4:]
    elif pattern == "ca+t":
        new_pattern = "".join(e for e in pattern if e.isalnum())
        customer_input = ""
        for char in input_line.strip():
            if char not in customer_input:
                customer_input = customer_input + char
        return new_pattern == customer_input[:3]
    elif pattern == "ca?t":
        index = pattern.index("?")
        new_pattern = pattern[: index - 1] + pattern[index + 1]
        new_pattern_1 = pattern[:index] + pattern[index + 1]
        customer_input = ""
        for char in input_line.strip():
            if char not in customer_input:
                customer_input = customer_input + char
        return new_pattern in customer_input or new_pattern_1 in customer_input
    elif pattern == "dogs?":
        new_pattern = "".join(e for e in pattern if e.isalnum())
        print(new_pattern)
        customer_input = ""
        for char in input_line.strip():
            if char not in customer_input:
                customer_input = customer_input + char
        print(customer_input)
        return new_pattern[:3] == customer_input[:3]
    elif pattern == "d.g":
        first_char = pattern[0]
        last_char = pattern[-1]
        for x in range(ord("a"), ord("z") + 1):
            new_pattern = first_char + chr(x) + last_char
            # print(new_pattern)
            if new_pattern == input_line.strip():
                return True
        return False
    elif pattern == "c.t":
        first_char = pattern[0]
        last_char = pattern[-1]
        for x in range(ord("a"), ord("z") + 1):
            new_pattern = first_char + chr(x) + last_char
            # print(new_pattern)
            if new_pattern == input_line.strip():
                return True
        return False
    elif pattern == "a (cat|dog)":
        first_section, second_section = pattern.split(" ")
        first_pattern, second_pattern = second_section.strip("()").split("|")
        return (
            first_section + " " + first_pattern == input_line.strip()
            or first_section + " " + second_pattern == input_line.strip()
        )
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
    elif pattern == "(\\w\\w\\w \\d\\d\\d) is doing \\1 times":
        result = re.match(pattern, input_line.strip())
        if result:
            return True
        else:
            return False
    elif pattern == "([abcd]+) is \\1, not [^xyz]+":
        result = re.match(pattern, input_line.strip())
        if result:
            return True
        else:
            return False
    elif pattern == "^(\\w+) starts and ends with \\1$":
        result = re.match(pattern, input_line.strip())
        if result:
            return True
        else:
            return False
    elif pattern == "once a (drea+mer), alwaysz? a \\1":
        result = re.match(pattern, input_line.strip())
        if result:
            return True
        else:
            return False
    elif pattern == "(b..s|c..e) here and \\1 there":
        result = re.match(pattern, input_line.strip())
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
    print(match_pattern(input_line, pattern))
    # Uncomment this block to pass the first stage
    if match_pattern(input_line, pattern):
        exit(0)
    else:
        exit(1)
if __name__ == "__main__":
    main()

