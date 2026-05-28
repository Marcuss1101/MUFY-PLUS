from groq import Groq
import json

client = Groq(api_key=GROQ_API_KEY)

MODEL = "llama-3.1-8b-instant"


def generate_ai_quiz():
    prompt = """
Generate a quiz in STRICT JSON format.

Rules:
- 5 questions
- each question must have:
  - question (string)
  - options (array of 4 strings)
  - answer (string must match one option exactly)

Return ONLY JSON.

Format:
{
  "quiz": [
    {
      "question": "...",
      "options": ["A", "B", "C", "D"],
      "answer": "A"
    }
  ]
}
"""

    res = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You output only valid JSON."},
            {"role": "user", "content": prompt}
        ]
    )

    return res.choices[0].message.content