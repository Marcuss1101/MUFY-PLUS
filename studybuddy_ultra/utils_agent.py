import os
from groq import Groq
from utils_storage import load, save

# ---------------- CONFIG ----------------
MODEL = "llama-3.1-8b-instant"
FILE = "data/stats.json"

# ---------------- SAFE API INIT ----------------
api_key = "GROQ_API_KEY"  # Set this in your environment for AI features
if not api_key:
    client = None
else:
    client = Groq(api_key=api_key)


# ---------------- AUTONOMOUS STUDY PLAN ----------------
def generate_plan():
    stats = load(FILE)

    weak = stats.get("weak_subjects", {})

    prompt = f"""
You are an autonomous study AI.

Weak subjects (higher number = weaker priority):
{weak}

Generate:
1. Today's study plan (3 tasks)
2. Priority subject
3. Short revision summary

Keep it structured and simple.
"""

    try:
        if client is None:
            return "⚠️ Groq API key not set. Please set GROQ_API_KEY in environment."

        res = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are an autonomous study planner AI."},
                {"role": "user", "content": prompt}
            ]
        )

        return res.choices[0].message.content

    except Exception as e:
        return f"AI Error: {str(e)}"


# ---------------- AUTONOMOUS QUIZ GENERATOR ----------------
def generate_quiz():
    stats = load(FILE)
    weak = stats.get("weak_subjects", {})

    prompt = f"""
Create a 5-question exam quiz based on weak subjects:
{weak}

Include answers at the end.
Make it moderately difficult.
"""

    try:
        if client is None:
            return "⚠️ Groq API key not set."

        res = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are an exam generator AI."},
                {"role": "user", "content": prompt}
            ]
        )

        return res.choices[0].message.content

    except Exception as e:
        return f"AI Error: {str(e)}"


# ---------------- PERFORMANCE UPDATE LOOP ----------------
def update_performance(score, subject):
    stats = load(FILE)

    stats["last_quiz_score"] = score

    if subject in stats["weak_subjects"]:
        if score < 70:
            stats["weak_subjects"][subject] += 1
        else:
            stats["weak_subjects"][subject] -= 1

    save(FILE, stats)