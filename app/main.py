import sys
import string
def match_pattern(initial_input_line: str, initial_pat: str):
    input_line = initial_input_line = initial_input_line.removesuffix("\n")
    initial_len = len(input_line)
    pat = initial_pat
    if pat == "":
        return True
    if input_line == "":
        return False
    backtrack_stack = [input_line]
    cap_groups = []
    cap_group_start = None
    while True:
        def try_match():
            nonlocal input_line, pat, initial_len
            # print(f"{input_line=!r} {pat=!r}")
            if pat.startswith("^"):
                if len(input_line) != initial_len:
                    return False
                pat = pat[1:]
                return True
            if pat.startswith("$"):
                if input_line != "":
                    return False
                pat = pat[1:]
                return True
            import sys
import string
def match_pattern(initial_input_line: str, initial_pat: str):
    input_line = initial_input_line = initial_input_line.removesuffix("\n")
    initial_len = len(input_line)
    pat = initial_pat
    if pat == "":
        return True
    if input_line == "":
        return False
    backtrack_stack = [input_line]
    cap_groups = []
    cap_group_start = None
    while True:
        def try_match():
            nonlocal input_line, pat, initial_len
            # print(f"{input_line=!r} {pat=!r}")
            if pat.startswith("^"):
                if len(input_line) != initial_len:
                    return False
                pat = pat[1:]
                return True
            if pat.startswith("$"):
                if input_line != "":
                    return False
                pat = pat[1:]
                return True
            if pat and len(pat) >= 2 and pat[0] == "\\" and pat[1].isdigit():
                target = ""
                pat = pat[1:]
                while pat and pat[0].isdigit():
                    target += pat[0]
                    pat = pat[1:]
                target = int(target) - 1
                if input_line.startswith(cap_groups[target]):
                    input_line = input_line[len(cap_groups[target]) :]
                    return True
                else:
                    return False
            if len(input_line) == 0:
                return False
            alt = set()
            anything = False
            positive = True
            if pat.startswith("\\d"):
                alt |= set(string.digits)
                pat = pat[2:]
            elif pat.startswith("\\w"):
                alt |= set(string.ascii_letters)
                alt |= set(string.digits)
                alt |= set("_")
                pat = pat[2:]
            elif pat.startswith("[^"):
                positive = False
                end = pat.find("]", 2)
                if end == -1:
                    raise RuntimeError(f"Non-matching bracket")
                alt |= set(pat[2:end])
                pat = pat[end + 1 :]
            elif pat.startswith("["):
                positive = True
                end = pat.find("]", 1)
                if end == -1:
                    raise RuntimeError(f"Non-matching bracket")
                alt |= set(pat[1:end])
                pat = pat[end + 1 :]
            else:
                if pat[0] == ".":
                    anything = True
                else:
                    alt |= set([pat[0]])
                pat = pat[1:]
            # TODO: Implement wildcard support for parens
            wildcard = None
            if pat.startswith("+"):
                wildcard = "+"
                pat = pat[1:]
            elif pat.startswith("?"):
                wildcard = "?"
                pat = pat[1:]
            n_matches = 0
            while len(input_line) > 0 and (
                anything or (input_line[0] in alt) == positive
            ):
                input_line = input_line[1:]
                n_matches += 1
                if wildcard in {None, "?"}:
                    break
            if wildcard in {None, "+"} and n_matches == 0:
                return False
            return True
        def handle_group_end(match_ok: bool):
            nonlocal cap_group_start, cap_groups, backtrack_stack
            cap_group_end = len(initial_input_line) - len(input_line)
            assert cap_group_start is not None
            if match_ok:
                cap_groups.append(initial_input_line[cap_group_start:cap_group_end])
            cap_group_start = None
            backtrack_stack.pop()
            # print(cap_groups)
        if pat.startswith("("):
            cap_group_start = len(initial_input_line) - len(input_line)
            backtrack_stack.append(input_line)
            pat = pat[1:]
        if pat.startswith(")"):
            handle_group_end(True)
            succeeded = True
            pat = pat[1:]
        else:
            succeeded = try_match()
        def drop_current_group():
            nonlocal pat
            level = 1
            while True:
                # print("group drop:", pat)
                if pat == "":
                    break
                elif pat[0] == "(":
                    level += 1
                    pat = pat[1:]
                elif pat[0] == ")":
                    level -= 1
                    pat = pat[1:]
                    if level == 0:
                        break
                else:
                    pat = pat[1:]
            if len(backtrack_stack) == 1:
                level -= 1
            if level != 0:
                raise RuntimeError("Unmatched paren")
        def drop_current_alt():
            nonlocal pat
            level = 1
            while True:
                # print("alt drop:", pat)
                if pat == "":
                    break
                elif pat[0] == "(":
                    level += 1
                    pat = pat[1:]
                elif pat[0] == ")":
                    level -= 1
                    if level == 0:
                        break
                    pat = pat[1:]
                else:
                    if pat[0] == "|" and level == 1:
                        return
                    else:
                        pat = pat[1:]
            if len(backtrack_stack) == 1:
                level -= 1
            if level != 0:
                raise RuntimeError("Unmatched paren")
        match pat, succeeded:
            case "", True:
                return True
            case _, True:
                if pat.startswith("|"):
                    drop_current_group()
                    handle_group_end(True)
                if len(pat) == 0:
                    return True
            case _, False:
                drop_current_alt()
                if pat.startswith(")"):
                    handle_group_end(False)
                    pat = pat[1:]
                if pat.startswith("|"):
                    input_line = backtrack_stack[-1]
                    pat = pat[1:]
                else:
                    cap_groups = []
                    cap_group_start = None
                    pat = initial_pat
                    input_line = backtrack_stack[-1] = backtrack_stack[-1][1:]
                    if len(input_line) == 0:
                        return False
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