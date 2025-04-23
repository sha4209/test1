import streamlit as st
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
# Load dataset
df = pd.read_csv("gym and diet recommendation1.csv")

st.set_page_config(page_title="Smart Fitness Recommender")
st.title("🏋️ Smart Fitness, Diet & Workout Recommendation")

# Encode categorical columns
label_encoders = {}
encoded_df = df.copy()

for col in ["Sex", "Hypertension", "Diabetes", "Level", "Fitness Goal", "Fitness Type",
            "Recommended Diet Plan", "Recommended Workout Plan"]:
    le = LabelEncoder()
    encoded_df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Train models
X = encoded_df[["Sex", "Age", "Height", "Weight", "Hypertension", "Diabetes", "BMI" ]]
y_level = encoded_df["Level"]
y_diet = encoded_df["Recommended Diet Plan"]
y_workout = encoded_df["Recommended Workout Plan"]

model_level = RandomForestClassifier()
model_level.fit(X, y_level)

model_diet = RandomForestClassifier()
model_diet.fit(X, y_diet)

model_workout = RandomForestClassifier()
model_workout.fit(X, y_workout)
# --- First Form ---
with st.form("user_input"):
    sex = st.selectbox("Sex", df["Sex"].unique())
    age = st.number_input("Age", 10, 100, 25)
    height = st.number_input("Height (in meters)", 1.0, 2.5, 1.7)
    weight = st.number_input("Weight (in kg)", 30, 200, 65)
    hypertension = st.selectbox("Hypertension", ["Yes", "No"])
    diabetes = st.selectbox("Diabetes", ["Yes", "No"])
    submit = st.form_submit_button("🔍 Predict My Plan")

if submit:
    bmi = round(weight / (height ** 2), 2)
    st.session_state.bmi = bmi
    st.session_state.sex = sex
    st.session_state.age = age
    st.session_state.height = height
    st.session_state.weight = weight
    st.session_state.hypertension = hypertension
    st.session_state.diabetes = diabetes

    st.markdown(f"📏 **Your BMI is:** `{bmi}`")

    input_data = [[
        label_encoders["Sex"].transform([sex])[0],
        age,
        height,
        weight,
        label_encoders["Hypertension"].transform([hypertension])[0],
        label_encoders["Diabetes"].transform([diabetes])[0],
        bmi
    ]]

    pred_level_code = model_level.predict(input_data)[0]
    pred_level = label_encoders["Level"].inverse_transform([pred_level_code])[0]
    st.success(f"🏷️ **Predicted Fitness Level:** `{pred_level}`")


# train mode
X = encoded_df[["Sex", "Age", "Height", "Weight", "Hypertension", "Diabetes", "BMI","Fitness Goal", "Fitness Type"]]
y_level = encoded_df["Level"]
y_diet = encoded_df["Recommended Diet Plan"]
y_workout = encoded_df["Recommended Workout Plan"]
model_level = RandomForestClassifier()
model_level.fit(X, y_level)

model_diet = RandomForestClassifier()
model_diet.fit(X, y_diet)

model_workout = RandomForestClassifier()
model_workout.fit(X, y_workout)
# --- Second Form ---
with st.form("user_input1"):
    st.write("If you're interested, fill this out:")
    goal = st.selectbox("Fitness Goal", df["Fitness Goal"].unique())
    ftype = st.selectbox("Fitness Type", df["Fitness Type"].unique())
    generate = st.form_submit_button("Generate my plan")

if generate:
    try:
        input_data = [[
            label_encoders["Sex"].transform([st.session_state.sex])[0],
            st.session_state.age,
            st.session_state.height,
            st.session_state.weight,
            label_encoders["Hypertension"].transform([st.session_state.hypertension])[0],
            label_encoders["Diabetes"].transform([st.session_state.diabetes])[0],
            st.session_state.bmi,
            label_encoders["Fitness Goal"].transform([goal])[0],
            label_encoders["Fitness Type"].transform([ftype])[0],
        ]]

        pred_level_code = model_level.predict(input_data)[0]
        pred_diet_code = model_diet.predict(input_data)[0]
        pred_workout_code = model_workout.predict(input_data)[0]

        pred_level = label_encoders["Level"].inverse_transform([pred_level_code])[0]
        pred_diet = label_encoders["Recommended Diet Plan"].inverse_transform([pred_diet_code])[0]
        pred_workout = label_encoders["Recommended Workout Plan"].inverse_transform([pred_workout_code])[0]

        st.success(f"🏷️ **Predicted Fitness Level:** `{pred_level}`")
        st.markdown("---")
        st.subheader("🍽️ Recommended Diet Plan")
        st.info(pred_diet)
        st.subheader("🏋️ Recommended Workout Plan")
        st.info(pred_workout)

    except AttributeError:
        st.error("⚠️ Please fill out the first form and click 'Predict My Plan' before generating your plan.")
