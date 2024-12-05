from dotenv import load_dotenv
import sys
from collections import Counter
from pathlib import Path

# Add the project root to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from utils.aoc_client import AocClient

def solve_part1(input_data: str) -> int:
    # Split input into lines and parse into two lists
    lines = input_data.strip().split('\n')
    left_list = []
    right_list = []

    for line in lines:
        left, right = line.split()
        left_list.append(int(left))
        right_list.append(int(right))

    # Sort both lists
    left_list.sort()
    right_list.sort()

    # Calculate total distance
    total_distance = sum(abs(l - r) for l, r in zip(left_list, right_list))

    return total_distance

def solve_part2(input_data: str) -> int:
    # Parse input
    lines = input_data.strip().split('\n')
    left_list = []
    right_list = []

    for line in lines:
        left, right = line.split()
        left_list.append(int(left))
        right_list.append(int(right))

    # Count occurrences in right list
    right_counts = Counter(right_list)

    # Calculate similarity score
    similarity_score = sum(num * right_counts[num] for num in left_list)

    return similarity_score

def main():
    # Test examples
    example_input = """3 4
4 3
2 5
1 3
3 9
3 3"""
    assert solve_part1(example_input) == 11, "Part 1 example failed!"
    assert solve_part2(example_input) == 31, "Part 2 example failed!"

    # Solve actual puzzle
    load_dotenv()
    client = AocClient()
    input_data = client.get_input(1)

    # Part 1
    answer1 = solve_part1(input_data)
    print(f"Part 1: {answer1}")

    # Part 2
    answer2 = solve_part2(input_data)
    print(f"Part 2: {answer2}")

    # Submit part 2
    response = client.submit_answer(1, 2, answer2)
    print(f"Submission response: {response}")

if __name__ == "__main__":
    main()
