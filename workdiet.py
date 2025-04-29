import base64
import streamlit as st
from streamlit_option_menu import option_menu
import time
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import requests
import os
# ---------------------- FUNCTION TO ENCODE IMAGE ----------------------
def encode_image_to_base64(image_path):
    """Reads an image file and encodes it as a Base64 string."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

# ---------------------- BACKGROUND IMAGE ----------------------
image_path = "youu.jpg"  # Ensure the correct path
image_base64 = encode_image_to_base64(image_path)

background_style = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("data:image/jpeg;base64,{image_base64}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
    height: 100vh;
    width: 100vw;
}}

h1, p {{
    color: white !important;
    font-weight: bold;
    text-align: center;
    font-size: 24px;
}}

.main-title {{
    font-size: 55px;
    font-weight: bold;
    text-shadow: 4px 4px 10px rgba(0, 0, 0, 1);
    margin-top: 50px;
}}

.button-container {{
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 30px;
}}

.stButton>button {{
    color: white !important;
    font-size: 24px !important;
    font-weight: bold !important;
    padding: 15px 30px !important;
    border: 2px solid white !important;
    border-radius: 12px !important;
    cursor: pointer !important;
    box-shadow: 0px 4px 10px rgba(255, 255, 255, 0.7) !important;
    transition: 0.3s ease-in-out !important;
}}

.stButton>button:hover {{
    background-color: #005f73 !important;
}}

.progress-bar {{
    background-color: #008CBA;
    height: 20px;
    border-radius: 10px;
    margin: 10px 0;
}}

.animated-text {{
    animation: fadeIn 2s ease-in-out;
}}

@keyframes fadeIn {{
    from {{ opacity: 0; }}
    to {{ opacity: 1; }}
}}
</style>
"""

st.markdown(background_style, unsafe_allow_html=True)

# ---------------------- WORKOUT & DIET PLANS ----------------------
def get_workout_plans():
    return {
        "beginner": [
            "✅ 30 min brisk walking", "✅ Bodyweight squats: 3x10", "✅ Push-ups: 3x5-10", "✅ Plank: 3x20-30 sec"
        ],
        "intermediate": [
            "✅ Jogging: 30 min", "✅ Dumbbell bench press: 3x10", "✅ Deadlifts: 3x10", "✅ Plank: 3x1 min"
        ],
        "advanced": [
            "🔥 HIIT: 20 min", "🔥 Barbell squats: 4x8", "🔥 Pull-ups: 4x5-10", "🔥 Plank with leg lift: 3x1 min"
        ]
    }

def get_diet_plans():
    return {
        "weight_loss": ["🥣 Oatmeal with fruits", "🥗 Grilled chicken salad", "🍲 Steamed veggies with fish", "🥜 Nuts & yogurt"],
        "muscle_gain": ["🍳 Eggs & whole grain toast", "🍛 Quinoa with chicken", "🐟 Brown rice & salmon", "💪 Protein shake"],
        "maintenance": ["🥤 Smoothie (spinach & banana)", "🥪 Turkey sandwich", "🥦 Stir-fried tofu", "🥕 Hummus with carrots"]
    }

def recommend_plan(fitness_level, goal):
    workout_plans = get_workout_plans()
    diet_plans = get_diet_plans()

    st.subheader("💪 Recommended Workout Plan:")
    for exercise in workout_plans.get(fitness_level, []):
        st.write(exercise)

    st.subheader("🍏 Recommended Diet Plan:")
    for meal in diet_plans.get(goal, []):
        st.write(meal)

#-------------------------------------------------------------------------


USER_DATA_FILE = "user.csv"

# Create CSV file if it doesn't exist
if not os.path.exists(USER_DATA_FILE):
    pd.DataFrame(columns=["Name", "Email", "Password"]).to_csv(USER_DATA_FILE, index=False)

# ---------------------- Session Initialization ----------------------
if "page" not in st.session_state:
    st.session_state.page = "home"
if "show_login" not in st.session_state:
    st.session_state.show_login = False
if "show_signup" not in st.session_state:
    st.session_state.show_signup = False

# ---------------------- Button Actions ----------------------
def on_login_click():
    st.session_state.show_login = True
    st.session_state.show_signup = False

def on_signup_click():
    st.session_state.show_signup = True
    st.session_state.show_login = False

# ---------------------- Home Page ----------------------
def show_home():
    st.markdown("<h1 style='text-align: center; color: #00bfff;'>TRAIN SMART</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>Workout & Diet Plan Recommendation System</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Personalized workout & diet recommendations based on your fitness goals.</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-style: italic;'>Give me a minute, I'm good. Give me an hour, I'm great. Give me six months, I'm unbeatable.</p>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([4, 3, 4])
    with c2:
        st.markdown("""
            <style>
                .stButton>button {
                    background-color: #00bfff;
                    color: white;
                    font-size: 18px;
                    padding: 10px 30px;
                    border: none;
                    border-radius: 10px;
                    cursor: pointer;
                }
                .stButton>button:hover {
                    background-color: #007acc;
                }
            </style>
        """, unsafe_allow_html=True)

        if st.button("🚀 Get Started"):
            st.session_state.page = "start"
            st.rerun()

# ---------------------- Start Page ----------------------
def show_start_page():
    st.markdown("<h1 style='text-align: center; color: #00bfff;'>TRAIN SMART</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center;'>Your Fitness & Diet Companion</h4>", unsafe_allow_html=True)

    st.markdown("""
        <style>
            .stButton>button {
                background-color: #00bfff;
                color: white;
                padding: 15px 40px;
                font-size: 18px;
                border: none;
                border-radius: 10px;
                cursor: pointer;
                transition: 0.3s;
            }
            .stButton>button:hover {
                background-color: #007acc;
            }
        </style>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    with col2:
        st.button("🔓 Login", on_click=on_login_click)
    with col3:
        st.button("✅ Sign Up", on_click=on_signup_click)

    if st.session_state.show_login:
        show_login_page()
    elif st.session_state.show_signup:
        show_signup_page()

# ---------------------- Login Page ----------------------
def show_login_page():
    st.subheader("🔒 Login Page")
    username = st.text_input("Username (Email)")
    password = st.text_input("Password", type="password")

    if st.button("🔓 Login Now"):
        if not username or not password:
            st.warning("⚠️ Please fill in both Username and Password.")
        else:
            users_df = pd.read_csv(USER_DATA_FILE)

            if username in users_df["Email"].values:
                user_row = users_df[users_df["Email"] == username]
                if user_row["Password"].values[0] == password:
                    user_name = user_row["Name"].values[0]
                    st.success(f"✅ Welcome back, {user_name}!")
                    st.session_state.user_name = user_name
                    st.session_state.page = "home_main"
                    st.session_state.show_login = False
                    st.session_state.show_signup = False
                    st.rerun()
                else:
                    st.error("❌ Incorrect Password")
            else:
                st.error("❌ User not found. Please sign up first.")

# ---------------------- Signup Page ----------------------
def show_signup_page():
    st.subheader("📝 Signup Page")
    new_name = st.text_input("Name", key="signup_name")
    new_username = st.text_input("Email", key="signup_email")
    new_password = st.text_input("Password", type="password", key="signup_pass")

    if st.button("✅ Sign Up Now"):
        if not new_username or not new_password or not new_name:
            st.warning("⚠️ Please fill in all the fields.")
        else:
            users_df = pd.read_csv(USER_DATA_FILE)

            if new_username in users_df["Email"].values:
                st.warning("⚠️ User already exists! Try logging in.")
            else:
                new_user = pd.DataFrame({
                    "Name": [new_name],
                    "Email": [new_username],
                    "Password": [new_password]
                })
                users_df = pd.concat([users_df, new_user], ignore_index=True)
                users_df.to_csv(USER_DATA_FILE, index=False)

                st.success("✅ Account created successfully!")
                st.session_state.show_signup = False
                st.session_state.show_login = True
                st.rerun()
# ---------------------- Main Home Page (Post Login) ----------------------

def show_home_main():
    
# elif st.session_state.page == "home_main":
# Set sidebar width and background color
    st.markdown("""
        <style>
            [data-testid="stSidebar"] {
                background-color: #262730;
                color: white;
                width: 250px;
            }
            .sidebar-title {
                font-size: 24px;
                font-weight: bold;
                color: #00bfff;
                text-align: center;
                padding: 10px;
            }
            .sidebar-footer {
                font-size: 12px;
                color: #bbbbbb;
                text-align: center;
                padding: 20px;
            }
        </style>
    """, unsafe_allow_html=True)

    # Sidebar navigation
# elif st.session_state.page == "home_main":
    with st.sidebar:
        st.markdown("<div class='sidebar-title'>🏋️‍♂️ TRAIN SMART </div>", unsafe_allow_html=True)

        selected = option_menu(
            menu_title='Navigation',
            options=['🏠 Home', '📊 Recommend', '🏋️ Workout Tips', '🥗 Diet Tips', '🍽️ Recipe','🎦 Video', '📞 Contact Us','🚪 Logout'],
            icons=['house', 'stars', 'stars', 'apple', 'book','stars', 'envelope','person'],
            menu_icon="list",  # Icon for the menu
            default_index=0,
            styles={
                "container": {"padding": "5px", "background-color": "#262730"},
                "icon": {"color": "#00bfff", "font-size": "20px"},
                "nav-link": {"font-size": "16px", "color": "white", "text-align": "left", "margin": "5px"},
                "nav-link-selected": {"background-color": "#00bfff", "color": "black", "font-weight": "bold"},
            }
        )



    if selected == "🏠 Home":
        st.title("🏋️‍♂️ Train Smart ")
        st.write("The Workout and Diet Plan Recommendation System is designed to help users achieve their fitness goals by providing personalized workout and diet plans based on their fitness level and specific objectives.")

        st.subheader("🛠️ 6 Steps to Create Your Own Fitness & Diet Plan")
        steps = ["1️⃣ Identify Your Goals", "2️⃣ Plan Your Workouts", "3️⃣ Create a Schedule",
                 "4️⃣ Determine Your Diet", "5️⃣ Create a Meal Plan", "6️⃣ Reevaluate Your Goals"]
        for step in steps:
            st.write(step)

        st.title("🏋️‍♂️ Which Age is Best for Gym?")
        c1, c2 = st.columns([1, 2])
        with c1:
            st.image("nutri.jpg")  
        with c2:
            st.write("While there's no single best age, around 17-18 is often considered a good time to start serious gym training, as muscles are more mature and can handle the demands of strength training. However, younger individuals can engage in supervised, age-appropriate activities. With proper supervision, younger teens (around 14-16) can also begin strength training safely.")
        
        st.subheader("🧐 Factors Influencing the Right Age to Start Gym Workouts")
        st.write("✅ **Physical Maturity:** The body reaches full physical maturity typically around ages 18-35, making this period ideal for more intense workouts.")
        st.write("✅ **Individual Goals:** Personal fitness goals can dictate when to start. For example, teenagers may focus on building a foundation, while young adults might aim for muscle building or fat loss.")
        st.write("✅ **Health Considerations:** Overall health and any pre-existing conditions should be evaluated before starting a gym routine, regardless of age.")

        st.title("Healthy Eating Plan")
        st.write("A healthy eating plan gives your body the nutrients it needs every day while staying within your daily calorie goal for weight loss. A healthy eating plan also will lower your risk for heart disease and other health conditions.")

        st.subheader("A healthy eating plan:")

        st.write("Emphasizes vegetables, fruits, whole grains, and fat-free or low-fat dairy products")
        st.write("Includes lean meats, poultry, fish, beans, eggs, and nuts")
        st.write("Limits saturated and trans fats, sodium, and added sugars")
        st.write("Controls portion sizes")
        st.subheader("Calories")
        st.write("To lose weight, most people need to reduce the number of calories they get from food and beverages (energy IN) and increase their physical activity (energy OUT).")

        st.write("For a weight loss of 1–1 ½ pounds per week, daily intake should be reduced by 500 to 750 calories. In general:")

        st.write("Eating plans that contain 1,200–1,500 calories each day will help most women lose weight safely.")
        st.write("Eating plans that contain 1,500–1,800 calories each day are suitable for men and for women who weigh more or who exercise regularly.")
        st.write(" Very low calorie diets of fewer than 800 calories per day should not be used unless you are being monitored by your doctor.")
        
        st.subheader("Click here to watch the video ")
        st.write("Diet Plan For Weight Loss | Best Foods To Eat Before & After Workout")
        st.write("https://www.youtube.com/watch?v=irpVyU_5w_U&pp=ygUMI2RhaXRpbmdwbGFu")
        st.write("How to Exercise & Diet Correctly for Your Body Type")
        st.write("https://www.youtube.com/watch?v=5z7c7NdcH7I")
        st.write(" 7 Day Fat Loss Diet Plan")
        st.write("https://www.youtube.com/watch?v=grcgXfejaug&pp=ygUMI2dtZGlldGNoYXJ0")
        st.write("Gym Diet Plan: Pre-Workout, Post Workout & 7-Day Gym Diet Chart")
        st.write("https://www.bajajallianz.com/blog/wellness/gym-diet-chart-pre-and-post-workout.html")
        
    


    elif selected == "📊 Recommend":
        def load_data():
            file_path = "gym and diet recommendation1.csv"  # Ensure the correct path
            df= pd.read_csv(file_path)
            df = df.drop_duplicates(subset=["Level", "Fitness Goal", "Recommended Workout Plan", "Recommended Diet Plan"])
            return df
        def filter_recommendations(df, levels, goals):
            return df[(df["Level"].isin(levels)) & (df["Fitness Goal"].isin(goals))]

        def display_recommendations(filtered_df):
            if filtered_df.empty:
                st.warning("⚠️ No recommendations found for the selected criteria!")
            else:
                for _, row in filtered_df.iterrows():
                    st.write(f"### 🏋️ Workout Plan for {row['Level']} - {row['Fitness Goal']}")
                    st.info(row["Recommended Workout Plan"])
                    
                    st.write(f"### 🍽️ Diet Plan for {row['Level']} - {row['Fitness Goal']}")
                    st.success(row["Recommended Diet Plan"])

        def main():
            st.subheader("📌 Get Your Personalized Plan")
            # df = load_data()
        df = pd.read_csv("gym and diet recommendation1.csv")

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
        st.subheader("📌 Get Your Personalized Plan")
        # --- First Form ---
        with st.form("user_input"):
            
            sex = st.selectbox("Sex", df["Sex"].unique())
            age = st.number_input("Age", 10, 100, 25)
            height = st.number_input("Height (in meters)", 1.0, 7.0, 1.7)
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

                    
       

            

    elif selected == "🏋️ Workout Tips":
       
        df = pd.read_csv("gym and diet recommendation1.csv")

        # Encode categorical columns
        label_encoders = {}
        for col in ['Fitness Type', 'Fitness Goal', 'Recommended Workout Plan', 'Recommended Diet Plan']:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col])
            label_encoders[col] = le

        # Define Features and Target
        X = df[['Fitness Type', 'Fitness Goal']]
        y_workout = df['Recommended Workout Plan']
        y_diet = df['Recommended Diet Plan']

        # Split Data
        X_train, X_test, y_workout_train, y_workout_test = train_test_split(X, y_workout, test_size=0.2, random_state=42)
        X_train, X_test, y_diet_train, y_diet_test = train_test_split(X, y_diet, test_size=0.2, random_state=42)

        # Train Random Forest Models
        rf_workout = RandomForestClassifier(n_estimators=100, random_state=42)
        rf_workout.fit(X_train, y_workout_train)

        rf_diet = RandomForestClassifier(n_estimators=100, random_state=42)
        rf_diet.fit(X_train, y_diet_train)

        # Streamlit UI
        st.title("Workout & Diet Plan Recommendation System")

        # User Inputs
        fitness_levels = label_encoders['Fitness Type'].classes_
        fitness_goals = label_encoders['Fitness Goal'].classes_

        fitness_level = st.selectbox("Select Your Fitness Level", fitness_levels)
        fitness_goal = st.selectbox("Select Your Fitness Goal", fitness_goals)

        if st.button("Get Recommendation"):
            # Convert user input to encoded values
            fitness_level_encoded = label_encoders['Fitness Type'].transform([fitness_level])[0]
            fitness_goal_encoded = label_encoders['Fitness Goal'].transform([fitness_goal])[0]

            # Predict Workout & Diet
            prediction_workout = rf_workout.predict([[fitness_level_encoded, fitness_goal_encoded]])[0]
            # prediction_diet = rf_diet.predict([[fitness_level_encoded, fitness_goal_encoded]])[0]

            # Decode Predictions
            recommended_workout = label_encoders['Recommended Workout Plan'].inverse_transform([prediction_workout])[0]
            # recommended_diet = label_encoders['Recommended Diet Plan'].inverse_transform([prediction_diet])[0]

            st.success(f"🏋️ Recommended Workout Plan: {recommended_workout}")
            # st.success(f"🥗 Recommended Diet Plan: {recommended_diet}")

    elif selected == "🥗 Diet Tips":
        
        df = pd.read_csv("gym and diet recommendation1.csv")

        # Function to calculate BMI category
        def get_bmi_category(bmi):
            if bmi < 18.5:
                return "Underweight"
            elif 18.5 <= bmi < 25:
                return "Normal"
            elif 25 <= bmi < 30:
                return "Overweight"
            else:
                return "Obese"

        # Title
        st.title("🥗 Personalized Diet Plan Recommendation")

        # User input fields
        age = st.number_input("Enter Your Age:", min_value=10, max_value=100, value=25, step=1)
        height = st.number_input("Enter Your Height (in meters):", min_value=1.0, max_value=100.5, value=1.75, step=0.01)
        weight = st.number_input("Enter Your Weight (in kg):", min_value=20.0, max_value=200.0, value=70.0, step=0.5)

        # Calculate BMI and determine fitness level
        if height > 0:
            bmi = round(weight / (height ** 2), 2)
            fitness_level = get_bmi_category(bmi)
            st.write(f"**Your BMI:** {bmi} ({fitness_level})")

        # Filter the dataset based on Age & Fitness Level
        filtered_df = df[(df["Age"] == age) & (df["Level"] == fitness_level)]

        # Show diet plan when button is clicked
        if st.button("Show Diet Plan"):
            if filtered_df.empty:
                st.warning("⚠️ No diet plan found for your criteria!")
            else:
                st.write(f"### 🍽️ Diet Plan for Age {age} - {fitness_level}")
                for idx, row in filtered_df.iterrows():
                    st.success(row["Recommended Diet Plan"])
                
        unique_diet_plans = filtered_df["Recommended Diet Plan"].drop_duplicates()

        for plan in unique_diet_plans:
                st.success(plan)

        
    elif selected == "📞 Contact Us":
        st.title("Train Smart")
        st.write("The Workout and Diet Plan Recommendation System is designed to assist users in achieving their fitness goals by providing personalized workout and diet plans. It considers factors such as fitness level, body composition, activity level, and specific objectives to generate effective recommendations.")

        st.subheader("📞 Contact Us")
        st.markdown("📩 Email: support@fitnessapp.com")
        st.write("📞 Phone: +123-456-7890")

    elif selected =="🍽️ Recipe":
# API details

        url = "https://ai-food-recipe-generator-api-custom-diet-quick-meals.p.rapidapi.com/generate"

        headers = {

            "x-rapidapi-key": "59cf561792mshab0b712d79987b4p1b7c74jsn03d7fcdc6dde",  # Replace with your API key

            "x-rapidapi-host": "ai-food-recipe-generator-api-custom-diet-quick-meals.p.rapidapi.com",

            "Content-Type": "application/json"

        }


        st.title("AI Recipe Generator")


        # User inputs

        ingredients = st.text_input("Enter ingredients (comma separated)")

        dietary_restrictions = st.multiselect("Select Dietary Restrictions", ["gluten_free", "vegan", "vegetarian", "nut_free", "dairy_free"])

        cuisine = st.selectbox("Select Cuisine", ["Italian", "Chinese", "Mexican", "Indian", "American"])

        meal_type = st.selectbox("Select Meal Type", ["breakfast", "lunch", "dinner", "snack"])

        servings = st.number_input("Number of Servings", min_value=1, value=4)


        if st.button("Generate Recipe"):

            # Convert inputs to appropriate format

            ingredients_list = [i.strip() for i in ingredients.split(",") if i.strip()]

            

            payload = {

                "ingredients": ingredients_list,

                "dietary_restrictions": dietary_restrictions,

                "cuisine": cuisine,

                "meal_type": meal_type,

                "servings": servings,

                "lang": "en"

            }

            

            querystring = {"noqueue": "1"}

            response = requests.post(url, json=payload, headers=headers, params=querystring)

            # response = requests.post(url, json=payload, headers=headers, params=querystring)

            # st.write(response.status_code)

            # st.write(response.text)

            

            if response.status_code == 200:

                data = response.json()

                st.subheader(f"Dish: {data['result']['title']}")

                st.subheader("Ingredients")

                for item in data['result']['ingredients']:

                    st.write(f"- {item['name']}: {item['amount']}")

                

                st.subheader("Instructions")

                for step in data['result']['instructions']:

                    st.write(step)

            else:

                st.error("Failed to fetch recipe. Please try again!")

    elif selected =="🎦 Video":
        c1, c2 ,c3= st.columns([2, 3,2])
        with c2:
            st.title(" TRAIN SMART ")
        st.write("Here’s a well-structured Video Page Content for your Workout and Diet Plan Recommendation System. This page will host workout tutorial videos or healthy recipe demos—ideal for motivating users and guiding them visually.")
        st.markdown("Click here to watch the video ")
        st.subheader("Diet Plan For Weight Loss | Best Foods To Eat Before & After Workout")
        st.video("https://www.youtube.com/watch?v=irpVyU_5w_U&pp=ygUMI2RhaXRpbmdwbGFu")
        st.subheader("How to Exercise & Diet Correctly for Your Body Type")
        st.video("https://www.youtube.com/watch?v=5z7c7NdcH7I")
        st.subheader(" 7 Day Fat Loss Diet Plan")
        st.video("https://www.youtube.com/watch?v=grcgXfejaug&pp=ygUMI2dtZGlldGNoYXJ0")
        st.subheader("Gym Diet Plan: Pre-Workout, Post Workout & 7-Day Gym Diet Chart")
        st.video("https://www.youtube.com/watch?v=yTM2EWaBui0")
    elif selected =="🚪 Logout":
        st.markdown("<h1 style='text-align: center; color: #FF5722;'>🏋️ Welcome to Train Smart</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Your fitness journey doesn't end here. Come back soon to stay on track 💪</p>", unsafe_allow_html=True)
        
        # st.title(f"👋 See you next time, {st.session_state.get('user_name', 'User')}!")
        col1, col2, col3  = st.columns([3, 2, 3])
        with col2:
            if st.button("🚪 Logout"):
                # user_name = st.session_state.get("user_name", "Champion")
                # st.success(f"👋 See you next time, {user_name}!")
                st.session_state.page = "start"
                st.session_state.show_login = False
                st.session_state.show_signup = False
                st.rerun() 
                st.title(f"👋 Hello, {st.session_state.get('user_name', 'User')}!") 
        st.markdown(f"""
<h2 style='text-align: center; color: #00bfff;'>👋 See you next time, {st.session_state.get('user_name', 'User')}!</h2>
<p style='text-align: center;'>You’ve taken one more step towards greatness. Rest up and come back stronger.</p>
<p style='text-align: center; font-style: italic;'>The grind never stops. But neither do you.</p>
""", unsafe_allow_html=True)

        
     
if st.session_state.page == "home":
    show_home()
elif st.session_state.page == "start":
    show_start_page()
elif st.session_state.page == "home_main":
    show_home_main()            