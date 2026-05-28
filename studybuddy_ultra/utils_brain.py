from groq import Groq
from utils_storage import load

client = Groq(api_key="YOUR_GROQ_API_KEY")

MODEL = "llama-3.1-70b-versatile"

FILE = "data/stats.json"


def generate_study_plan():
    stats = load(FILE)

    weak = stats.get("weak_subjects", [])

    prompt = f"""
You are a study AI planner.

Student weak subjects: {weak}

Create:
- 3 tasks for today
- 1 focus priority
- 1 short revision summary
Keep it simple and structured.
"""

    res = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are an expert study planner."},
            {"role": "user", "content": prompt}
        ]
    )

    return res.choices[0].message.content