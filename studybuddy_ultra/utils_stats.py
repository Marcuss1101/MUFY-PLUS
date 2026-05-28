from datetime import date
from utils_storage import load, save

FILE = "data/stats.json"

def get_stats():
    return load(FILE)

def add_xp(amount=10):
    stats = get_stats()

    stats["xp"] += amount
    stats["level"] = stats["xp"] // 100 + 1

    save(FILE, stats)
    return stats

def update_streak():
    stats = get_stats()
    today = str(date.today())

    if stats["last_active"] != today:
        if stats["last_active"] != "":
            stats["streak"] += 1

        stats["last_active"] = today

    save(FILE, stats)
    return stats