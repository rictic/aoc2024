from dotenv import load_dotenv
import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from utils.aoc_client import AocClient

def is_safe_report(levels: list[int]) -> bool:
    if len(levels) < 2:
        return True

    # Check first difference to determine if we should be increasing or decreasing
    diff = levels[1] - levels[0]
    if diff == 0:  # No change is unsafe
        return False

    expected_direction = 1 if diff > 0 else -1

    # Check each pair of numbers
    for i in range(len(levels) - 1):
        diff = levels[i + 1] - levels[i]
        # Must maintain direction
        if (diff > 0 and expected_direction < 0) or (diff < 0 and expected_direction > 0):
            return False
        # Must differ by 1-3
        if abs(diff) < 1 or abs(diff) > 3:
            return False

    return True

def solve_part1(input_data: str) -> int:
    # Parse input
    reports = []
    for line in input_data.strip().split('\n'):
        levels = [int(x) for x in line.split()]
        reports.append(levels)

    # Count safe reports
    return sum(1 for report in reports if is_safe_report(report))

def solve_part2(input_data: str) -> int:
    return 0  # Placeholder for part 2

def main():
    # Test examples
    example_input = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""

    result = solve_part1(example_input)
    assert result == 2, f"Part 1 example failed! Got {result} expected 2"

    # Solve actual puzzle
    load_dotenv()
    client = AocClient()
    input_data = client.get_input(2)

    # Part 1
    answer1 = solve_part1(input_data)
    print(f"Part 1: {answer1}")

    # Submit answer
    client.submit_answer(2, 1, str(answer1))

if __name__ == "__main__":
    main()
