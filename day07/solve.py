from dotenv import load_dotenv
import sys
from pathlib import Path
from itertools import product

# Add the project root to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from utils.aoc_client import AocClient

def evaluate_expression(nums, operators):
    """Evaluate expression from left to right"""
    result = nums[0]
    for i, op in enumerate(operators):
        if op == '+':
            result += nums[i + 1]
        elif op == '*':
            result *= nums[i + 1]
        else:  # op == '||'
            # Convert both numbers to strings, concatenate, then back to int
            result = int(str(result) + str(nums[i + 1]))
    return result

def can_make_target(target: int, nums: list[int], use_concat: bool = False) -> bool:
    """Check if target can be made from nums using operators"""
    num_operators = len(nums) - 1
    operators = ['+', '*']
    if use_concat:
        operators.append('||')
    # Try all possible combinations of operators
    for ops in product(operators, repeat=num_operators):
        try:
            if evaluate_expression(nums, ops) == target:
                return True
        except ValueError:
            # Skip if we create a number too large for int
            continue
    return False

def parse_line(line: str) -> tuple[int, list[int]]:
    """Parse a line into target value and list of numbers"""
    target_str, nums_str = line.split(':')
    target = int(target_str)
    nums = [int(x) for x in nums_str.strip().split()]
    return target, nums

def solve_part1(input_data: str) -> int:
    # Parse input
    lines = input_data.strip().split('\n')
    
    # Process each equation
    total = 0
    for line in lines:
        target, nums = parse_line(line)
        if can_make_target(target, nums):
            total += target
    
    return total

def solve_part2(input_data: str) -> int:
    # Parse input
    lines = input_data.strip().split('\n')
    
    # Process each equation
    total = 0
    for line in lines:
        target, nums = parse_line(line)
        if can_make_target(target, nums, use_concat=True):
            total += target
    
    return total

def main():
    # Test examples
    example_input = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""
    assert solve_part1(example_input) == 3749, "Part 1 example failed!"
    assert solve_part2(example_input) == 11387, "Part 2 example failed!"
    
    # Solve actual puzzle
    load_dotenv()
    client = AocClient()
    input_data = client.get_input(7)
    
    # Part 1
    answer1 = solve_part1(input_data)
    print(f"Part 1: {answer1}")
    
    # Part 2
    answer2 = solve_part2(input_data)
    print(f"Part 2: {answer2}")
    
    # Submit part 2
    response = client.submit_answer(7, 2, str(answer2))
    print(f"Submission response: {response}")

if __name__ == "__main__":
    main()