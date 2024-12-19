from flask import Flask, request, jsonify
import itertools
from collections import Counter
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

def validate_inputs(previous_draw, month, day):
    """
    Validate the inputs for the draw, month, and day.
    """
    if not (1000 <= previous_draw <= 9999):
        raise ValueError("Previous draw must be a 4-digit number.")
    if not (1 <= month <= 12):
        raise ValueError("Month must be between 1 and 12.")
    if not (1 <= day <= 31):
        raise ValueError("Day must be between 1 and 31.")

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
        for j, transform in enumerate(transformations.values(), start=1):
            grid[i][j] = transform(grid[i][0])
    
    return grid

def calculate_date_sum(month, day):
    """
    Calculate the date sum and return the last digit.
    """
    return (month + day) % 10

def find_pattern(grid, pattern="8396"):
    """
    Search for a specific pattern in the grid, including rows, columns, and diagonals.
    """
    pattern_variants = ["".join(p) for p in itertools.permutations(pattern)]
    pattern_found = []
    rows = ["".join(map(str, row)) for row in grid]
    cols = ["".join(map(str, col)) for col in zip(*grid)]
    diagonals = [
        "".join(str(grid[i][i]) for i in range(4)),
        "".join(str(grid[i][3 - i]) for i in range(4))
    ]
    
    for line in itertools.chain(rows, cols, diagonals):
        for variant in pattern_variants:
            if variant in line:
                pattern_found.append((line, variant))
    
    return pattern_found

def analyze_draw(previous_draw, month, day):
    """
    Analyze the draw and identify patterns.
    """
    # Validate inputs
    validate_inputs(previous_draw, month, day)
    
    # Convert previous draw to integers
    previous_draw = list(map(int, str(previous_draw)))
    
    # Step 1: Generate the grid
    grid = generate_grid(previous_draw)
    
    # Step 2: Calculate date sum
    date_sum = calculate_date_sum(month, day)
    
    # Step 3: Find patterns
    patterns = find_pattern(grid)
    
    # Step 4: Assign weights to patterns
    pattern_weights = Counter([match[1] for match in patterns])
    weighted_patterns = {key: value / sum(pattern_weights.values()) for key, value in pattern_weights.items()}
    
    return {
        "grid": grid,
        "date_sum": date_sum,
        "patterns": patterns,
        "weighted_patterns": weighted_patterns,
    }

@app.route("/analyze", methods=["POST"])
def analyze():
    """
    Analyze lottery draws based on user input.
    """
    try:
        data = request.json
        if not data:
            raise ValueError("Missing request body.")

        previous_draw = data.get("previous_draw")
        month = data.get("month")
        day = data.get("day")

        if previous_draw is None or month is None or day is None:
            raise ValueError("Missing 'previous_draw', 'month', or 'day'.")

        # Logging for debug purposes
        logging.info(f"Received data: {data}")

        # Perform analysis
        result = analyze_draw(int(previous_draw), int(month), int(day))
        return jsonify(result), 200

    except ValueError as ve:
        logging.error(f"Validation error: {ve}")
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        logging.error(f"Internal server error: {e}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    # Run the Flask app locally
    app.run(debug=True)
