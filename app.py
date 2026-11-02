from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)
model = joblib.load("model/maternal_model.pkl")
cols = joblib.load("model/model_columns.pkl")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    row = pd.get_dummies(pd.DataFrame([data]))
    row = row.reindex(columns=cols, fill_value=0).astype(float)
    pred = int(model.predict(row)[0])
    prob = float(model.predict_proba(row)[0][1])
    return jsonify({"high_risk": pred, "probability": round(prob, 3)})

if __name__ == "__main__":
    app.run(port=5000)
    