
import streamlit as st
import json
import os
from datetime import datetime

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

feeling_text = st.text_area(
    "How are you feeling today?",
    placeholder="Example: I feel tired and my legs are sore..."
)

# -------------------------------
# AI Response Function
# -------------------------------
def ai_reply(feeling_text, energy, mood, fatigue):
    text = feeling_text.lower()
    
    # Simple rule-based replies
    if "tired" in text or fatigue >= 7:
        reply = "I see you are tired today. Let's focus on rest and gentle activity."
    elif "pain" in text or "sore" in text:
        reply = "Oh no! I suggest light stretching and avoiding heavy exercise."
    elif "happy" in text or mood >= 8:
        reply = "Great to hear! Keep up your positive energy today!"
    elif feeling_text.strip() == "":
        reply = "Thanks for logging in! Let's plan your day."
    else:
        reply = "Got it! I'll make sure today's plan suits how you're feeling."
    
    return reply

# -------------------------------
# AI Daily Plan Generator
# -------------------------------
def generate_daily_plan(energy, mood, fatigue, feeling_text):
    plan = {}
    text = feeling_text.lower()
    
    # Exercise
    if "pain" in text or "sore" in text:
        plan["Exercise"] = "Skip exercise today and rest"
    elif fatigue >= 7:
        plan["Exercise"] = "Light stretching (10–15 min)"
    else:
        plan["Exercise"] = "Normal walk or exercise (20–30 min)"
    
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
    
    # Medication (dummy time for now)
    plan["Medication"] = "Take medication at 12:00 PM"
    
    return plan

# -------------------------------
# Generate Plan Button
# -------------------------------
if st.button("Generate My Daily Plan"):
    daily_plan = generate_daily_plan(energy, mood, fatigue, feeling_text)
    reply = ai_reply(feeling_text, energy, mood, fatigue)
    
    # Display AI reply
    st.markdown(f"**🤖 AI says:** {reply}")
    
    # Show plan
    st.subheader("📝 Your Personalized Daily Plan")
    for k, v in daily_plan.items():
        st.write(f"**{k}:** {v}")
    
    # Save log
    log_entry = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "energy": energy,
        "mood": mood,
        "fatigue": fatigue,
        "feeling_text": feeling_text,
        "ai_reply": reply,
        "plan": daily_plan
    }
    user_state["logs"].append(log_entry)
    
    # Update streak
    user_state["streak"] += 1
    st.success(f"✅ Log saved! Your Consistency Days streak: {user_state['streak']}")
    
    # Save to JSON
    with open(STATE_FILE, "w") as f:
        json.dump(user_state, f, indent=4)

# -------------------------------
# Gamification / Family Messages
# -------------------------------
st.header("🏆 Gamification & Family Encouragement")
if user_state["streak"] % 5 == 0 and user_state["streak"] != 0:
    st.balloons()
    st.info(f"🎉 Awesome! You've reached {user_state['streak']} Consistency Days!")
    st.write("Family says: 'Great job keeping up with your health today! ❤️'")

# -------------------------------
# Past Logs
# -------------------------------
st.header("📊 Past Logs & Plans (Last 5 Entries)")
if user_state["logs"]:
    for i, log in enumerate(reversed(user_state["logs"][-5:]), 1):
        st.markdown(f"**Entry {i} ({log['date']}):**")
        st.write(f"Energy: {log['energy']}, Mood: {log['mood']}, Fatigue: {log['fatigue']}")
        st.write(f"Feeling: {log['feeling_text']}")
        st.write(f"AI Reply: {log['ai_reply']}")
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


