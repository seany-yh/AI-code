import streamlit as st
import json
import os
from datetime import datetime, date

# ----------------------------
# Load persistent state
# ----------------------------
STATE_FILE = "user_state.json"

if os.path.exists(STATE_FILE):
    with open(STATE_FILE, "r") as f:
        user_state = json.load(f)
else:
    user_state = {}

# Ensure all required keys exist
user_state.setdefault("logs", [])
user_state.setdefault("streak", 0)
user_state.setdefault("last_log_date", None)
user_state.setdefault("chat_history", [])
def save_state():
    with open(STATE_FILE, "w") as f:
        json.dump(user_state, f, indent=4)

# ----------------------------
# Consecutive day streak logic
# ----------------------------
def update_streak():
    today = date.today()

    if user_state["last_log_date"] is None:
        user_state["streak"] = 1
    else:
        last_date = datetime.strptime(user_state["last_log_date"], "%Y-%m-%d").date()
        diff = (today - last_date).days

        if diff == 1:
            user_state["streak"] += 1
        elif diff > 1:
            user_state["streak"] = 1

    user_state["last_log_date"] = today.strftime("%Y-%m-%d")

# ----------------------------
# AI Chatbot Brain
# ----------------------------
def ai_chatbot_response(message):
    msg = message.lower()

    # Health-related responses
    if "tired" in msg:
        return "You seem tired today. I recommend more rest and gentle activity."
    if "pain" in msg or "sore" in msg:
        return "I suggest light stretching and avoiding heavy exercise."
    if "medication" in msg:
        return "Please remember to take your medication on schedule."
    if "appointment" in msg:
        return "I will remind you about upcoming medical appointments."
    if "diet" in msg or "food" in msg:
        return "Try to maintain a balanced meal with less sugar and salt."
    if "sad" in msg or "stress" in msg:
        return "I'm here for you. Consider resting or speaking with a loved one."

    return "Thank you for sharing. I will adjust your support plan accordingly."

# ----------------------------
# Daily plan generator
# ----------------------------
def generate_daily_plan(energy, mood, fatigue, notes):
    plan = {}

    if fatigue >= 7 or "tired" in notes.lower():
        plan["Exercise"] = "Light stretching or short walk"
        plan["Rest"] = "Extra rest recommended"
    else:
        plan["Exercise"] = "Normal walk (20–30 minutes)"
        plan["Rest"] = "Normal rest schedule"

    if mood <= 3:
        plan["Wellness"] = "Relaxation activity or talk to family"
    else:
        plan["Wellness"] = "Maintain normal routine"

    plan["Medication"] = "Take medication as prescribed"

    return plan

# ----------------------------
# UI CONFIG
# ----------------------------
st.set_page_config(page_title="AI Health Tablet", layout="wide")
st.title("💊 AI Health Tablet")

# =====================================================
# 💬 CHATBOT INTERFACE
# =====================================================
st.header("💬 Talk to Your Health AI")

# Display chat history
for chat in user_state["chat_history"]:
    with st.chat_message("user"):
        st.write(chat["user"])
    with st.chat_message("assistant"):
        st.write(chat["ai"])

# Chat input box (real chat UI)
user_message = st.chat_input("Type your message here...")

if user_message:
    ai_response = ai_chatbot_response(user_message)

    user_state["chat_history"].append({
        "user": user_message,
        "ai": ai_response
    })

    save_state()
    st.rerun()

# =====================================================
# 📋 DAILY HEALTH CHECK-IN
# =====================================================
st.header("📋 Daily Health Check-In")

col1, col2, col3 = st.columns(3)

with col1:
    energy = st.slider("Energy Level", 0, 10, 5)

with col2:
    mood = st.slider("Mood", 0, 10, 5)

with col3:
    fatigue = st.slider("Fatigue", 0, 10, 3)

notes = st.text_area("Describe how you feel today")

if st.button("Generate My Daily Plan"):
    update_streak()

    plan = generate_daily_plan(energy, mood, fatigue, notes)
    reply = ai_chatbot_response(notes)

    st.subheader("🤖 AI Feedback")
    st.write(reply)

    st.subheader("📝 Today's Plan")
    for k, v in plan.items():
        st.write(f"**{k}:** {v}")

    user_state["logs"].append({
        "date": date.today().strftime("%Y-%m-%d"),
        "energy": energy,
        "mood": mood,
        "fatigue": fatigue,
        "notes": notes,
        "plan": plan
    })

    save_state()
    st.success(f"Logged! Consistency Days: {user_state['streak']}")

# =====================================================
# 🏆 GAMIFICATION
# =====================================================
st.header("🏆 Progress")
st.metric("Consistency Days", user_state["streak"])

if user_state["streak"] > 0 and user_state["streak"] % 5 == 0:
    st.balloons()
    st.info("🎉 Amazing consistency! Your family is proud of you ❤️")

# =====================================================
# 📊 HISTORY
# =====================================================
st.header("📊 Recent Logs")

if user_state["logs"]:
    for log in reversed(user_state["logs"][-5:]):
        st.write(f"Date: {log['date']}")
        st.write(f"Energy: {log['energy']} | Mood: {log['mood']} | Fatigue: {log['fatigue']}")
        st.write(f"Notes: {log['notes']}")
        for k, v in log["plan"].items():
            st.write(f"- {k}: {v}")
        st.write("---")
else:
    st.write("No logs yet.")
