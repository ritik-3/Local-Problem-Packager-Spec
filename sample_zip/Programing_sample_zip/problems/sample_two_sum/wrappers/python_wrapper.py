import sys
import json

# User solution is injected here
# USER_CODE_START
def two_sum(nums, target):
    return []
# USER_CODE_END

def run_test(test_input, expected_output):
    try:
        lines = test_input.strip().split('\n')
        n = int(lines[0])
        nums = list(map(int, lines[1].split()))
        target = int(lines[2])

        result = two_sum(nums, target)
        output = ' '.join(map(str, result))

        return output.strip() == expected_output.strip()
    except Exception as e:
        return False

if __name__ == "__main__":
    # Read input and expected output from stdin/env
    test_input = sys.stdin.read()
    result = two_sum([2, 7, 11, 15], 9)
    print(' '.join(map(str, result)))