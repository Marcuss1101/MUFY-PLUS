import re

def parse_quiz(raw_text):
    questions = []

    blocks = raw_text.split("Q:")

    for b in blocks:
        if not b.strip():
            continue

        try:
            q_part = b.split("A)")[0].strip()

            options = re.findall(r"[A-D]\) (.*)", b)
            answer_line = [line for line in b.split("\n") if "Answer:" in line]

            answer = answer_line[0].replace("Answer:", "").strip() if answer_line else ""

            questions.append({
                "question": q_part,
                "options": options,
                "answer": answer
            })
        except:
            continue

    return questions