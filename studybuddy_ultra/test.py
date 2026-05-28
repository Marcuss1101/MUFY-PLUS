from groq import Groq

client = Groq(api_key=GROQ_API_KEY)

res = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[{"role": "user", "content": "Say hello"}]
)

print(res.choices[0].message.content)