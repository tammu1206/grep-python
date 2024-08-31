import sys
import re

def match_pattern(input_line, pattern):
    # Initialize regex pattern string
    regex_pattern = ''

    # Split pattern into segments
    segments = pattern.split(' ')
    
    for segment in segments:
        if segment == r"\d":
            regex_pattern += r'\d'
        elif segment == r"\w":
            regex_pattern += r'\w'
        elif segment.startswith('[') and segment.endswith(']'):
            if segment[1] == '^':
                excluded_chars = set(segment[2:-1])
                regex_pattern += f'[^{''.join(excluded_chars)}]'
            else:
                allowed_chars = set(segment[1:-1])
                regex_pattern += f'[{''.join(allowed_chars)}]'
        else:
            # Escape literal text
            regex_pattern += re.escape(segment)

    # Compile the final regex pattern
    regex = re.compile(f'^{regex_pattern}$')
    
    # Match the input line against the compiled regex pattern
    match = regex.match(input_line)
    return match is not None

def main():
    if len(sys.argv) != 3:
        print("Usage: ./your_program.sh -E '<pattern>'")
        exit(1)

    pattern = sys.argv[2]
    input_line = sys.stdin.read().strip()

    if sys.argv[1] != "-E":
        print("Expected first argument to be '-E'")
        exit(1)

    # Check if the input line matches the pattern
    if match_pattern(input_line, pattern):
        exit(0)
    else:
        exit(1)

if __name__ == "__main__":
    main()
