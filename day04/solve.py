from dotenv import load_dotenv
import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from utils.aoc_client import AocClient

def find_xmas(grid: list[str], row: int, col: int) -> list[tuple[int, int, int, int]]:
    """Check all 8 directions from a starting position for 'XMAS'."""
    height, width = len(grid), len(grid[0])
    directions = [
        (0, 1),   # right
        (1, 0),   # down
        (1, 1),   # diagonal down-right
        (-1, 1),  # diagonal up-right
        (0, -1),  # left
        (-1, 0),  # up
        (-1, -1), # diagonal up-left
        (1, -1),  # diagonal down-left
    ]

    found = []
    for dy, dx in directions:
        # Check if XMAS fits in this direction
        if (0 <= row + 3*dy < height and
            0 <= col + 3*dx < width and
            grid[row][col] == 'X' and
            grid[row + dy][col + dx] == 'M' and
            grid[row + 2*dy][col + 2*dx] == 'A' and
            grid[row + 3*dy][col + 3*dx] == 'S'):
            found.append((row, col, row + 3*dy, col + 3*dx))
    return found

def solve_part1(input_data: str) -> int:
    # Convert input into grid
    grid = input_data.strip().split('\n')

    # Search for XMAS in all directions from each starting position
    all_xmas = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            all_xmas.extend(find_xmas(grid, i, j))

    return len(all_xmas)

def find_xmas_part2(grid: list[str], row: int, col: int) -> list[tuple[int, int, int, int, int, int]]:
    """Check for X patterns where A is center, and each diagonal has M and S at ends."""
    height, width = len(grid), len(grid[0])

    # Define the two possible X patterns:
    # Each tuple contains (dy1, dx1, dy2, dx2) for the two diagonal directions
    x_patterns = [
        ((1, 1), (-1, 1)),   # down-right and up-right
        ((1, -1), (-1, -1)), # down-left and up-left
    ]

    found = []
    for (dy1, dx1), (dy2, dx2) in x_patterns:
        # Check if pattern fits
        if (0 <= row + dy1 < height and
            0 <= col + dx1 < width and
            0 <= row + dy2 < height and
            0 <= col + dx2 < width and
            0 <= row - dy1 < height and
            0 <= col - dx1 < width and
            0 <= row - dy2 < height and
            0 <= col - dx2 < width):

            # Get all characters in the potential pattern
            center = grid[row][col]
            end1 = grid[row + dy1][col + dx1]
            end2 = grid[row - dy1][col - dx1]
            end3 = grid[row + dy2][col + dx2]
            end4 = grid[row - dy2][col - dx2]

            # Debug print for each potential pattern
            if center == 'A':
                print(f"Checking at ({row}, {col}):")
                print(f"  Center: {center}")
                print(f"  Diagonal 1 ends: {end1}, {end2}")
                print(f"  Diagonal 2 ends: {end3}, {end4}")

            # Check center is A
            if center != 'A':
                continue

            # For each diagonal, one end must be M and the other S
            if not ((end1 == 'M' and end2 == 'S') or (end1 == 'S' and end2 == 'M')):
                continue
            if not ((end3 == 'M' and end4 == 'S') or (end3 == 'S' and end4 == 'M')):
                continue

            # Only add the pattern if we haven't seen it before
            # Sort the coordinates to ensure we only count each pattern once
            coords = sorted([
                (row + dy1, col + dx1),
                (row - dy1, col - dx1),
                (row + dy2, col + dx2),
                (row - dy2, col - dx2)
            ])
            pattern = (row, col, *coords[0], *coords[1], *coords[2], *coords[3])
            found.append(pattern)
            print(f"  Found valid pattern!")
    return found

def solve_part2(input_data: str) -> int:
    # Convert input into grid
    grid = input_data.strip().split('\n')

    print("\nGrid:")
    for line in grid:
        print(line)
    print()

    # Search for X-MAS patterns from each starting position
    all_xmas = set()  # Using a set to avoid duplicates
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            patterns = find_xmas_part2(grid, i, j)
            for pattern in patterns:
                all_xmas.add(pattern)

    print(f"\nTotal patterns found: {len(all_xmas)}")
    return len(all_xmas)

def main():
    # Test examples
    example_input = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""

    assert solve_part1(example_input) == 18, "Part 1 example failed!"
    assert solve_part2(example_input) == 9, "Part 2 example failed!"

    # Solve actual puzzle
    load_dotenv()
    client = AocClient()
    input_data = client.get_input(4)

    # Part 1
    answer1 = solve_part1(input_data)
    print(f"Part 1: {answer1}")
    response = client.submit_answer(4, 1, answer1)
    print(f"Submission response: {response}")
    # Part 2 (when available)
    answer2 = solve_part2(input_data)
    print(f"Part 2: {answer2}")
    response = client.submit_answer(4, 2, answer2)
    print(f"Submission response: {response}")

if __name__ == "__main__":
    main()
