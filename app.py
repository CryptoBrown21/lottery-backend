from flask import Flask, request, jsonify
import random

app = Flask(name)

Prediction Logic

def predict_hit_enhanced(initial_draw, date, historical_data=None):
A, B, C, D = [int(d) for d in str(initial_draw)]
A_plus2, A_plus5 = (A + 2) % 10, (A + 5) % 10
B_plus2, B_plus5 = (B + 2) % 10, (B + 5) % 10
C_plus2, C_plus5 = (C + 2) % 10, (C + 5) % 10
D_plus2, D_plus5 = (D + 2) % 10, (D + 5) % 10
Center = round((A + B + C + D) / 4) % 10
Center_plus1 = (Center + 1) % 10
Center_plus2 = (Center_plus1 + 1) % 10
month, day = [int(d) for d in date.split('-')]
date_sum = (month + day) % 10
mirror_map = {0: 5, 1: 6, 2: 7, 3: 8, 4: 9, 5: 0, 6: 1, 7: 2, 8: 3, 9: 4}
mirror = mirror_map[date_sum]
circled_numbers = [date_sum, mirror]
prediction_grid = [
[A_plus2, mirror, B_plus2],
[date_sum, Center_plus1, Center_plus2],
[C_plus2, date_sum, D_plus2]
]
predicted_hits = [
(num, 2) if num in circled_numbers else (num, 1)
for row in prediction_grid for num in row
]
if historical_data:
predicted_hits = sorted(predicted_hits, key=lambda x: random.random())
return {
"grid": prediction_grid,
"predicted_hits": [num for num, weight in predicted_hits if weight > 1]
}

@app.route("/predict", methods=["POST"])
def predict():
try:
data = request.json  # Get JSON data from the POST request
initial_draw = data.get("initial_draw")
date = data.get("date")
if not initial_draw or not date:
return jsonify({"error": "Missing 'initial_draw' or 'date'"}), 400
result = predict_hit_enhanced(initial_draw, date)
return jsonify(result), 200
except Exception as e:
return jsonify({"error": str(e)}), 500

if name == "main":
app.run(debug=True)

