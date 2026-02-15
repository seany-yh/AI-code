import streamlit as st
import json
import os

# -------------------------------
# Load or initialize user state
# -------------------------------
STATE_FILE = "user_state.json"

if os.path.exists(STATE_FILE):
    with open(STATE_FILE, "r") as f:
        user_state = json.load(f)
else:
    user_state = {
        "logs": [],
        "streak": 0
    }

# -------------------------------
# App Header
# -------------------------------
st.set_page_config(page_title="AI Health Tablet", layout="wide")
st.title("💊 AI Health Tablet")

# -------------------------------
# Daily Check-In
# -------------------------------
st.header("📋 Daily Check-In")

col1, col2, col3 = st.columns(3)

with col1:
    energy = st.slider("Energy Level", 0, 10, 5)

with col2:
    mood = st.slider("Mood", 0, 10, 5)

with col3:
    fatigue = st.slider("Fatigue", 0, 10, 3)

# Free-text input for daily feeling
feeling_text = st.text_area(
    "Tell me how you are feeling today",
    placeholder="Example: I feel tired and my legs are sore..."
)

# Dummy risk level for demonstration (could integrate real health risk later)
risk = "medium"

# -------------------------------
# AI Daily Plan Generator
# -------------------------------
def generate_daily_plan(energy, mood, fatigue, risk, feeling_text):
    plan = {}

    text = feeling_text.lower()

    # Exercise
    if "pain" in text or "sore" in text:
        plan["Exercise"] = "Skip exercise today and rest"
    elif risk == "high":
        plan["Exercise"] = "Light stretching (10–15 min)"
    elif risk == "medium":
        plan["Exercise"] = "Short walk (20 min)"
    else:
        plan["Exercise"] = "Normal walk or exercise (30 min)"

    # Rest
    if fatigue >= 7 or "tired" in text:
        plan["Rest"] = "Extra rest recommended today"
    else:
        plan["Rest"] = "Normal rest schedule"

    # Emotional wellness
    if mood <= 3 or "sad" in text or "stress" in text:
        plan["Wellness"] = "Relaxing activity or talk to family"
    else:
        plan["Wellness"] = "Maintain normal activities"

    # Medication reminder (demo)
    plan["Medication"] = "Take medication at 12:00 PM"

    return plan

# -------------------------------
# Generate plan button
# -------------------------------
if st.button("Generate My Daily Plan"):
    daily_plan = generate_daily_plan(energy, mood, fatigue, risk, feeling_text)
    
    # Show plan
    st.subheader("📝 Your Personalized Daily Plan")
    for k, v in daily_plan.items():
        st.write(f"**{k}:** {v}")
    
    # Save log
    log_entry = {
        "energy": energy,
        "mood": mood,
        "fatigue": fatigue,
        "feeling_text": feeling_text,
        "plan": daily_plan
    }
    user_state["logs"].append(log_entry)
    
    # Update streak
    user_state["streak"] += 1
    st.success(f"✅ Log saved! Your current streak: {user_state['streak']} days")
    
    # Save to JSON
    with open(STATE_FILE, "w") as f:
        json.dump(user_state, f, indent=4)

# -------------------------------
# Show past logs
# -------------------------------
st.header("📊 Past Logs & Plans")
if user_state["logs"]:
    for i, log in enumerate(reversed(user_state["logs"][-5:]), 1):
        st.markdown(f"**Entry {i}:**")
        st.write(f"Energy: {log['energy']}, Mood: {log['mood']}, Fatigue: {log['fatigue']}")
        st.write(f"Feeling: {log['feeling_text']}")
        st.write("Plan:")
        for k, v in log["plan"].items():
            st.write(f"- {k}: {v}")
        st.write("---")
else:
    st.write("No logs yet. Start by filling in your daily check-in above!")

# -------------------------------
# Footer
# -------------------------------
st.markdown("Made with ❤️ for elderlies’ health management")
