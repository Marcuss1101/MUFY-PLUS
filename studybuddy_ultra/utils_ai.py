from groq import Groq

client = Groq(api_key=GROQ_API_KEY)

MODEL = "llama-3.1-8b-instant"


def ask_ai(prompt, mode="explain"):
    prompts = {
        "explain": "Explain clearly step by step for students.",
        "quiz": "Generate 5 MCQs with answers.",
        "summary": "Summarize into key revision points.",
        "planner": "Create a study plan.",
    }

    try:
        res = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": prompts.get(mode, prompts["explain"])},
                {"role": "user", "content": prompt}
            ]
        )
        return res.choices[0].message.content
    except Exception as e:
        return f"AI Error: {e}"