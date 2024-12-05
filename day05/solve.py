from dotenv import load_dotenv
import sys
from collections import defaultdict
from pathlib import Path
from typing import List, Dict, Set, Tuple

# Add the project root to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from utils.aoc_client import AocClient

def parse_input(input_data: str) -> Tuple[Dict[int, Set[int]], List[List[int]]]:
    # Split into rules and updates sections
    rules_section, updates_section = input_data.strip().split('\n\n')
    
    # Parse rules into graph of dependencies
    # Key: page number, Value: set of pages that must come BEFORE this page
    dependencies = defaultdict(set)
    for rule in rules_section.split('\n'):
        before, after = map(int, rule.split('|'))
        dependencies[after].add(before)
    
    # Parse updates into lists of page numbers
    updates = []
    for update in updates_section.split('\n'):
        pages = list(map(int, update.split(',')))
        updates.append(pages)
        
    return dependencies, updates

def build_dependency_graphs(pages: List[int], dependencies: Dict[int, Set[int]]) -> Tuple[Dict[int, Set[int]], Dict[int, Set[int]]]:
    """Build both before and after dependency graphs just for the pages in this update."""
    before = defaultdict(set)  # things that must come before a page
    after = defaultdict(set)   # things that must come after a page
    
    # For each page, check what must come before it
    for page in pages:
        for dep in dependencies[page]:
            if dep in pages:  # Only include dependencies within our update
                before[page].add(dep)
                after[dep].add(page)
    
    return before, after

def is_valid_order(pages: List[int], dependencies: Dict[int, Set[int]]) -> bool:
    """Check if the order satisfies all dependencies."""
    for i, page in enumerate(pages):
        required_before = dependencies[page]
        actual_before = set(pages[:i])
        # Check if any required pages are missing from actual pages before this one
        if not required_before.issubset(actual_before):
            missing_required = required_before - actual_before
            if any(req in pages for req in missing_required):
                return False
    return True

def find_valid_order(pages: List[int], dependencies: Dict[int, Set[int]]) -> List[int]:
    """Find a valid ordering of the pages that satisfies all dependencies."""
    if len(pages) <= 1:
        return pages
        
    # Build both before and after dependency graphs
    before_deps, after_deps = build_dependency_graphs(pages, dependencies)
    
    # Track which pages we've used
    remaining = set(pages)
    result = []
    
    while remaining:
        # Find a page that has no remaining dependencies before it
        # and maximizes the number of remaining pages that must come after it
        best_page = None
        max_after = -1
        
        for page in remaining:
            # Count dependencies that must come before this page
            before_count = sum(1 for p in before_deps[page] if p in remaining)
            if before_count == 0:
                # Count how many remaining pages must come after this one
                after_count = sum(1 for p in after_deps[page] if p in remaining)
                if after_count > max_after:
                    max_after = after_count
                    best_page = page
        
        if best_page is None:
            # If we can't find a valid page, there must be a cycle
            # Return pages in their original order
            return pages
            
        result.append(best_page)
        remaining.remove(best_page)
    
    return result

def solve_part1(input_data: str) -> int:
    # Parse input
    dependencies, updates = parse_input(input_data)
    
    # Find valid updates and their middle numbers
    total = 0
    for update in updates:
        if is_valid_order(update, dependencies):
            middle_idx = len(update) // 2
            total += update[middle_idx]
            
    return total

def solve_part2(input_data: str) -> int:
    # Parse input
    dependencies, updates = parse_input(input_data)
    
    # Find invalid updates and fix their order
    total = 0
    for update in updates:
        if not is_valid_order(update, dependencies):
            # Find valid ordering for this update
            fixed_order = find_valid_order(update, dependencies)
            # Add middle number
            middle_idx = len(fixed_order) // 2
            total += fixed_order[middle_idx]
            
    return total

def main():
    # Test examples
    example_input = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""

    assert solve_part1(example_input) == 143, "Part 1 example failed!"
    assert solve_part2(example_input) == 123, "Part 2 example failed!"
    
    # Solve actual puzzle
    load_dotenv()
    client = AocClient()
    input_data = client.get_input(5)
    
    # Part 1
    answer1 = solve_part1(input_data)
    print(f"Part 1: {answer1}")
    
    # Part 2
    answer2 = solve_part2(input_data)
    print(f"Part 2: {answer2}")
    
    # Submit part 2
    response = client.submit_answer(5, 2, str(answer2))
    print(f"Submission response: {response}")

if __name__ == "__main__":
    main()