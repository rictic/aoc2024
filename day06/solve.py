from dotenv import load_dotenv
import sys
from pathlib import Path
from typing import Set, Tuple, Optional
from copy import deepcopy

# Add the project root to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from utils.aoc_client import AocClient

def parse_map(input_data: str) -> tuple[list[str], tuple[int, int, str]]:
    """Parse the input map and return the grid and guard starting position with direction."""
    lines = input_data.strip().split('\n')
    grid = []
    guard_pos = None
    
    for i, line in enumerate(lines):
        row = list(line)
        if '^' in line or '>' in line or 'v' in line or '<' in line:
            j = line.find('^')
            if j != -1:
                guard_pos = (i, j, '^')
            j = line.find('>')
            if j != -1:
                guard_pos = (i, j, '>')
            j = line.find('v')
            if j != -1:
                guard_pos = (i, j, 'v')
            j = line.find('<')
            if j != -1:
                guard_pos = (i, j, '<')
            row[guard_pos[1]] = '.'  # Replace guard with empty space
        grid.append(row)
    
    return grid, guard_pos

def get_next_pos(pos: tuple[int, int], direction: str) -> tuple[int, int]:
    """Get the next position based on current position and direction."""
    row, col = pos
    if direction == '^':
        return (row - 1, col)
    elif direction == '>':
        return (row, col + 1)
    elif direction == 'v':
        return (row + 1, col)
    else:  # '<'
        return (row, col - 1)

def turn_right(direction: str) -> str:
    """Return the new direction after turning right 90 degrees."""
    return {'^': '>', '>': 'v', 'v': '<', '<': '^'}[direction]

def simulate_guard(grid: list[str], start_pos: tuple[int, int, str], detect_loop: bool = False, max_steps: int = 10000) -> Optional[set[tuple[int, int]]]:
    """
    Simulate guard movement and return set of visited positions.
    If detect_loop is True, returns None if guard exits the map.
    """
    height, width = len(grid), len(grid[0])
    visited = {(start_pos[0], start_pos[1])}
    
    # Only track state history if we're detecting loops
    state_history = {(start_pos[0], start_pos[1], start_pos[2])} if detect_loop else set()
    
    # Current state
    row, col = start_pos[0], start_pos[1]
    direction = start_pos[2]
    
    for _ in range(max_steps):
        # Check if position in front is blocked or out of bounds
        next_row, next_col = get_next_pos((row, col), direction)
        
        if (next_row < 0 or next_row >= height or 
            next_col < 0 or next_col >= width or 
            grid[next_row][next_col] == '#'):
            # Turn right
            direction = turn_right(direction)
        else:
            # Move forward
            row, col = next_row, next_col
            visited.add((row, col))
            
            # Check if we've left the map
            if row == height - 1 or row == 0 or col == width - 1 or col == 0:
                if detect_loop:
                    return None
                break
            
            # Check for loop if we're detecting them
            if detect_loop:
                state = (row, col, direction)
                if state in state_history:
                    return visited
                state_history.add(state)
    
    return visited

def solve_part1(input_data: str) -> int:
    # Parse input
    grid, guard_start = parse_map(input_data)
    visited = simulate_guard(grid, guard_start)
    return len(visited)

def solve_part2(input_data: str) -> int:
    # Parse input
    grid, guard_start = parse_map(input_data)
    height, width = len(grid), len(grid[0])
    
    # Try each possible position for new obstacle
    valid_positions = 0
    
    for row in range(height):
        for col in range(width):
            # Skip if position is already occupied or is guard start
            if (grid[row][col] != '.' or 
                (row == guard_start[0] and col == guard_start[1])):
                continue
            
            # Try adding obstacle here
            new_grid = deepcopy(grid)
            new_grid[row][col] = '#'
            
            # Simulate guard movement with loop detection
            result = simulate_guard(new_grid, guard_start, detect_loop=True)
            
            # If we got a result (not None), it means guard got stuck in a loop
            if result is not None:
                valid_positions += 1
    
    return valid_positions

def main():
    # Test example
    example_input = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""
    assert solve_part1(example_input) == 41, "Part 1 example failed!"
    assert solve_part2(example_input) == 6, "Part 2 example failed!"
    
    # Solve actual puzzle
    load_dotenv()
    client = AocClient()
    input_data = client.get_input(6)
    
    # Part 1
    answer1 = solve_part1(input_data)
    print(f"Part 1: {answer1}")
    
    # Part 2
    answer2 = solve_part2(input_data)
    print(f"Part 2: {answer2}")
    
    # Submit answer
    response = client.submit_answer(6, 2, str(answer2))
    print(f"Submission response: {response}")

if __name__ == "__main__":
    main()