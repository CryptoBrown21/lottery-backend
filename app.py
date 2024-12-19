from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# Core Logic Functions
def generate_grid(previous_draw):
    grid = [[0] * 4 for _ in range(4)]
    transformations = {
        "plus_one": lambda x: (x + 1) % 10,
        "minus_one": lambda x: (x - 1) % 10,
        "mirror": lambda x: (x + 5) % 10,
    }

    for i, digit in enumerate(previous_draw):
        grid[i][0] = digit

    for i in range(4):
        for j, transform in enumerate(transformations.values(), start=1):
            grid[i][j] = transform(grid[i][0])

    return grid

def calculate_date_sum(month, day):
    return (month + day) % 10

def find_pattern(grid, pattern="8396"):
    import itertools
    pattern_found = []
    rows = ["".join(map(str, row)) for row in grid]
    cols = ["".join(map(str, col)) for col in zip(*grid)]

    for line in itertools.chain(rows, cols):
        if pattern in line:
            pattern_found.append(line)

    return pattern_found

def analyze_draw(previous_draw, month, day):
    previous_draw = list(map(int, str(previous_draw)))
    grid = generate_grid(previous_draw)
    date_sum = calculate_date_sum(month, day)
    patterns = find_pattern(grid)

    return {
        "grid": grid,
        "date_sum": date_sum,
        "patterns": patterns,
    }

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    previous_draw = data.get("previous_draw")
    month = data.get("month")
    day = data.get("day")

    if not previous_draw or not month or not day:
        return jsonify({"error": "Missing 'previous_draw', 'month', or 'day'"}), 400

    try:
        result = analyze_draw(int(previous_draw), int(month), int(day))
        return jsonify(result), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(debug=True)
