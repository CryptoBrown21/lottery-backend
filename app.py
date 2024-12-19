from flask import Flask, request, jsonify
import random

app = Flask(__name__)

def generate_grid(previous_draw):
    """
    Generate a 4x4 grid from the previous draw and apply transformations.
    """
    grid = [[0] * 4 for _ in range(4)]
    transformations = {
        "plus_one": lambda x: (x + 1) % 10,
        "minus_one": lambda x: (x - 1) % 10,
        "mirror": lambda x: (x + 5) % 10,
    }
    
    # Fill the first column with the previous draw digits
    for i, digit in enumerate(previous_draw):
        grid[i][0] = digit
    
    # Apply transformations
    for i in range(4):
        for j, (name, transform) in enumerate(transformations.items(), start=1):
            grid[i][j] = transform(grid[i][0])
    
    return grid

def calculate_date_sum(month, day):
    """
    Calculate the date sum and return the last digit.
    """
    return (month + day) % 10

def find_pattern(grid, pattern="8396"):
    """
    Search for a specific pattern in the grid.
    """
    pattern_found = []
    rows = ["".join(map(str, row)) for row in grid]
    cols = ["".join(map(str, col)) for col in zip(*grid)]
    
    for line in itertools.chain(rows, cols):
        if pattern in line:
            pattern_found.append(line)
    
    return pattern_found

def analyze_draw(previous_draw, month, day):
    """
    Analyze the draw and identify patterns.
    """
    # Convert previous draw to integers
    previous_draw = list(map(int, str(previous_draw)))
    
    # Step 1: Generate the grid
    grid = generate_grid(previous_draw)
    
    # Step 2: Calculate date sum
    date_sum = calculate_date_sum(month, day)
    
    # Step 3: Find patterns
    patterns = find_pattern(grid)
    
    return {
        "grid": grid,
        "date_sum": date_sum,
        "patterns": patterns,
    }

# Example usage
if __name__ == "__main__":
    # Input parameters
    previous_draw = 1474
    month = 12  # December
    day = 7
    
    # Analyze draw
    analysis = analyze_draw(previous_draw, month, day)
    
    # Display results
    print("Generated Grid:")
    for row in analysis["grid"]:
        print(row)
    
    print(f"\nDate Sum: {analysis['date_sum']}")
    print(f"Identified Patterns: {analysis['patterns']}")
