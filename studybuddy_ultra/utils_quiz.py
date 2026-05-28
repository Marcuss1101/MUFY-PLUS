from groq import Groq
from utils_storage import load

client = Groq(api_key=GROQ_API_KEY)
MODEL = "llama-3.1-8b-instant"

FILE = "data/stats.json"


def generate_ai_quiz():
    stats = load(FILE)

    weak = stats.get("weak_subjects", {})

    prompt = f"""
You are an AI Quizizz generator.

Create a 5-question multiple choice quiz.

Weak subjects:
{weak}

Rules:
- 4 options per question
- only 1 correct answer
- format clearly like:

Q: ...
A) ...
B) ...
C) ...
D) ...
Answer: B
"""

    res = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You generate quizzes for students."},
            {"role": "user", "content": prompt}
        ]
    )

    return res.choices[0].message.content