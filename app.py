from flask import Flask, request, jsonify

app = Flask(__name__)  # This 'app' is what Gunicorn looks for

@app.route('/')
def home():
    return "Lottery Prediction Backend is Running!"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    initial_draw = data.get("initial_draw")
    date = data.get("date")
    predicted_hits = [int(d) for d in str(initial_draw)]  # Simple mock logic
    return jsonify({"predicted_hits": predicted_hits})

if __name__ == '__main__':
    app.run(debug=True)
