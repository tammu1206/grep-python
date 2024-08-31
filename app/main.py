import os
import sys
from io import IOBase, StringIO
# import pyparsing - available if you need it!
# import lark - available if you need it!
_is_verbose = "VERBOSE" in os.environ
# List of subgroup matchers
references = []
def _d(s: str, end="\n"):
    if not _is_verbose:
        return
    print(s, file=sys.stderr, end=end)
def _literal_matcher(c: str):
    def m(f: StringIO):
        s = f.read(1)
        _d(f"{s} == {c}?")
        return s == c
    return m
def _group_matcher(chars: str, is_pos: bool):
    def m(f: StringIO) -> bool:
        s = f.read(1)
        res = s and (s in chars) == is_pos
        _d(f'{s} {"" if is_pos else "not "}in {chars}? {res}')
        return res
    return m
def _endline_matcher():
    def m(f: StringIO):
        s = f.read(1)
        _d(f'end? {s == ""}')
        return s == "" or s == "\n"
    return m
def _word_matcher():
    def m(f: StringIO):
        s = f.read(1)
        return s.isalnum() or s == "_"
    return m
def _zero_more_matcher(pm):
    def m(f: StringIO):
        while True:
            pos = f.tell()
            if not pm(f):
                f.seek(pos)
                break
        return True
    return m
def _zero_one_matcher(pm):
    def m(f: StringIO) -> bool:
        pos = f.tell()
        if not pm(f):
            f.seek(pos)
        return True
    return m
def _wildcard_matcher(f: StringIO) -> bool:
    s = f.read(1)
    return s != "" or s != "\n"
class SubgroupMatcher(object):
    matchers = []
    def __init__(self, choices):
        self.choices = choices
    def __call__(self, f: StringIO) -> bool:
        for choice in self.choices:
            _d("try choice")
            pos = f.tell()
            if choice(f):
                l = f.tell() - pos
                f.seek(pos)
                result = f.read(l)
                self.matchers = [_literal_matcher(c) for c in result]
                _d(f'choice "{result}" matches')
                return True
            f.seek(pos)
        return False
    def back_matcher(self, f: IOBase) -> bool:
        pos = f.tell()
        if all(m(f) for m in self.matchers):
            return True
        f.seek(pos)
        return False
def _subgroup_matcher(pf):
    choices = []
    while True:
        nm = pattern_to_matcher(pf, ["|", "(", ")"])
        c = pf.read(1)
        if c == "|":
            _d("add choice")
            choices.append(nm)
        elif c == ")":
            _d("add choice")
            choices.append(nm)
            _d("finish choice")
            break
        elif c == "(":
            choices.append(_subgroup_matcher(pf))
        else:
            raise Exception(f"Unknown char in subgroup: {c}")
    def m(f):
        for choice in choices:
            _d("try choice")
            pos = f.tell()
            if choice(f):
                _d("choice matches")
                return True
            f.seek(pos)
        return False
    return SubgroupMatcher(choices)
def _next_matcher(pf: IOBase, end):
    pos = pf.tell()
    c = pf.read(1)
    if c in end:
        pf.seek(pos)
        return None
    matcher = None
    if c == "\\":
        c = pf.read(1)
        if c == "d":
            matcher = lambda f: f.read(1).isdigit()
        elif c == "w":
            matcher = _word_matcher()
        elif c.isdigit():
            _d(f"back reference matcher: {c}")
            matcher = references[int(c) - 1].back_matcher
        else:
            matcher = _literal_matcher(c)
    elif c == "[":
        c = pf.read(1)
        is_neg = c == "^"
        chars = "" if is_neg else c
        while (c := pf.read(1)) != "]":
            chars += c
        _d(f"group matcher for: {chars}")
        matcher = _group_matcher(chars, not is_neg)
    elif c == "(":
        _d("subgroup matcher")
        matcher = _subgroup_matcher(pf)
        references.append(matcher)
    elif c == "$":
        _d("end matcher")
        matcher = _endline_matcher()
    elif c == ".":
        _d("wildcard matcher")
        matcher = _wildcard_matcher
    else:
        _d(f"literal matcher for: {c}")
        matcher = _literal_matcher(c)
    # Check repeater
    pos = pf.tell()
    c = pf.read(1)
    if c == "+":
        _d("one or more matcher")
        m = matcher
        matcher = lambda f: m(f) and _zero_more_matcher(m)(f)
    elif c == "*":
        _d("zero or more matcher")
        matcher = _zero_more_matcher(matcher)
    elif c == "?":
        _d("zero or one matcher")
        matcher = _zero_one_matcher(matcher)
    else:
        pf.seek(pos)
    return matcher
def _only_start_matcher(matchers):
    def m(f: StringIO) -> bool:
        for m in matchers:
            if not m(f):
                return False
        return True
    return m
def _scan_matcher(matchers):
    def m(f: StringIO) -> bool:
        c = "start"
        while c:
            pos = f.tell()
            for m in matchers:
                if not m(f):
                    f.seek(pos)
                    break
            else:
                return True
            c = f.read(1)
        return False
    return m
def pattern_to_matcher(pf: StringIO, end=["", "\n"]):
    pos = pf.tell()
    is_start = pf.read(1) == "^"
    if not is_start:
        pf.seek(pos)
    matchers = []
    for m in iter(lambda: _next_matcher(pf, end), None):
        _d("add matcher")
        matchers.append(m)
    if is_start:
        _d("_only_start_matcher")
        return _only_start_matcher(matchers)
    else:
        _d("_scan_matcher")
        return _scan_matcher(matchers)
def match_pattern(input_line: str, pattern: str):
    matcher = pattern_to_matcher(StringIO(pattern))
    return matcher(StringIO(input_line))
def main():
    pattern = sys.argv[2]
    input_line = sys.stdin.read()
    if sys.argv[1] != "-E":
        print("Expected first argument to be '-E'")
        exit(1)
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")
    if match_pattern(input_line, pattern):
        exit(0)
    else:
        exit(1)
if __name__ == "__main__":
    main()
