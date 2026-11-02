import streamlit as st
import requests

st.title("Maternal Health Risk Predictor")
st.write("Enter the mother's details to check pregnancy risk.")

sev = {"None": 0, "Minimal": 1, "Medium": 2, "Higher": 3}

col1, col2 = st.columns(2)
with col1:
    age = st.number_input("Age", 12, 50, 22)
    gravida = st.selectbox("Gravida (which pregnancy)", [1, 2, 3, 4])
    tetanus = st.selectbox("Tetanus vaccine dose", [1, 2, 3])
    gest = st.number_input("Gestational age (weeks)", 1, 42, 28)
    weight = st.number_input("Weight (kg)", 30.0, 120.0, 55.0)
    ft = st.number_input("Height (feet)", 4, 6, 5)
    inch = st.number_input("Height (inches)", 0, 11, 2)
with col2:
    anemia = st.selectbox("Anemia", list(sev.keys()))
    albumin = st.selectbox("Urine albumin", list(sev.keys()))
    jaundice = st.selectbox("Jaundice", ["No", "Yes"])
    fetal_pos = st.selectbox("Fetal position", ["Normal", "Abnormal"])
    fhr = st.number_input("Fetal heart rate", 80, 200, 132)
    sys_bp = st.number_input("Systolic BP", 70, 200, 100)
    dia_bp = st.number_input("Diastolic BP", 40, 130, 65)
    hrsag = st.selectbox("HRsAG", ["Negative", "Positive"])

if st.button("Predict"):
    data = {
        "Age": age,
        "Gravida": gravida,
        "Tetanus_Vaccine": tetanus,
        "Gestational_Age_Weeks": gest,
        "Weight_KG": weight,
        "Anemia": sev[anemia],
        "Fetal_Heart_Rate": fhr,
        "Urine_Albumin": sev[albumin],
        "Systolic_BP": sys_bp,
        "Diastolic_BP": dia_bp,
        "Height_CM": (ft * 12 + inch) * 2.54,
        "has_jaundice": 1 if jaundice == "Yes" else 0,
        "Fetal_Position": fetal_pos,
        "HRsAG": hrsag,
    }
    try:
        r = requests.post("http://127.0.0.1:5000/predict", json=data).json()
        if r["high_risk"] == 1:
            st.error(f"High risk (probability {r['probability']})")
        else:
            st.success(f"Not high risk (probability {r['probability']})")
    except Exception as e:
        st.warning("Couldn't reach the backend. Is app.py still running?")