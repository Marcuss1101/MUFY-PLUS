import random

MISSIONS = [
    "Complete 3 tasks",
    "Study for 25 minutes",
    "Do 1 AI quiz",
    "Summarize one topic",
    "Revise weak subject"
]


def get_mission():
    return random.choice(MISSIONS)