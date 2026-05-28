from datetime import date
from utils_storage import load, save

FILE = "data/stats.json"


def get():
    return load(FILE)


def add_xp(amount):
    s = get()

    xp_gain = amount * s.get("multiplier", 1)
    s["xp"] += xp_gain
    s["level"] = s["xp"] // 100 + 1

    save(FILE, s)
    return s


def add_badge(name):
    s = get()
    if name not in s["badges"]:
        s["badges"].append(name)
    save(FILE, s)


def update_streak():
    s = get()
    today = str(date.today())

    if s["last_active"] != today:
        if s["last_active"] != "":
            s["streak"] += 1
        s["last_active"] = today

    save(FILE, s)
    return s


def set_multiplier(val):
    s = get()
    s["multiplier"] = val
    save(FILE, s)