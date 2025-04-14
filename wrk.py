import streamlit as st

# Sample workout plans
workout_plans = {
    "beginner": [
        "30 minutes of brisk walking",
        "Bodyweight squats: 3 sets of 10 reps",
        "Push-ups: 3 sets of 5-10 reps",
        "Plank: 3 sets of 20-30 seconds"
    ],
    "intermediate": [
        "Jogging: 30 minutes",
        "Dumbbell bench press: 3 sets of 10 reps",
        "Deadlifts: 3 sets of 10 reps",
        "Plank: 3 sets of 1 minute"
    ],
    "advanced": [
        "High-intensity interval training (HIIT): 20 minutes",
        "Barbell squats: 4 sets of 8 reps",
        "Pull-ups: 4 sets of 5-10 reps",
        "Plank with leg lift: 3 sets of 1 minute"
    ]
}

# Sample diet plans
diet_plans = {
    "weight_loss": [
        "Breakfast: Oatmeal with fruits",
        "Lunch: Grilled chicken salad",
        "Dinner: Steamed vegetables with fish",
        "Snacks: Nuts and yogurt"
    ],
    "muscle_gain": [
        "Breakfast: Eggs and whole grain toast",
        "Lunch: Quinoa with chicken and vegetables",
        "Dinner: Brown rice with salmon",
        "Snacks: Protein shake and fruits"
    ],
    "maintenance": [
        "Breakfast: Smoothie with spinach and banana",
        "Lunch: Turkey sandwich with whole grain bread",
        "Dinner: Stir-fried tofu with vegetables",
        "Snacks: Hummus with carrots"
    ]
}

# Function to recommend plans
def recommend_plan(fitness_level, goal):
    st.subheader("Recommended Workout Plan:")
    workout_plan = workout_plans.get(fitness_level)
    if workout_plan:
        for exercise in workout_plan:
            st.write(f"- {exercise}")
    else:
        st.write("Invalid fitness level.")

    st.subheader("Recommended Diet Plan:")
    diet_plan = diet_plans.get(goal)
    if diet_plan:
        for meal in diet_plan:
            st.write(f"- {meal}")
    else:
        st.write("Invalid goal.")

# Streamlit app layout
st.markdown("""
    <style>
    body {
        background-color: #f0f2f5;
        font-family: 'Arial', sans-serif;
    }
    .header {
        background-color: #4CAF50;
        color: white;
        padding: 20px;
        text-align: center;
        border-radius: 10px;
    }
    .main {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        margin-top: 20px;
    }
    h1 {
        margin: 0;
    }
    h2 {
        color: #333;
    }
    .btn {
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s;
    }
    .btn:hover {
        background-color: #45a049;
    }
    .selectbox {
        margin-bottom: 20px;
    }
    .footer {
        text-align: center;
        margin-top: 20px;
        color: #777;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="header"><h1>Workout and Diet Plan Recommendation System</h1></div>', unsafe_allow_html=True)

# Main content
# st.markdown('<div class="main">', unsafe_allow_html=True)

# User input for fitness level
fitness_level = st.selectbox("Select your fitness level:", ["beginner", "intermediate", "advanced"], key="fitness_level", index=0)

# User input for goal
goal = st.selectbox("Select your goal:", ["weight_loss", "muscle_gain", "maintenance"], key="goal", index=0)

# Display recommendations
if st.button("Get Recommendations", key="recommend"):
    recommend_plan(fitness_level, goal)