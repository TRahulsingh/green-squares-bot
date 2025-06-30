import os
import random
import datetime
import subprocess
import json
import pytz  # For IST time formatting

# 🌿 Inspirational quotes
quotes = [
    "Push yourself, because no one else is going to do it for you.",
    "Success is the sum of small efforts, repeated.",
    "Small steps every day.",
    "One more brick in the wall of progress.",
    "Consistency is more important than intensity.",
    "Another line, another win!",
    "Stay curious, keep learning.",
    "Another commit to greatness.",
    "Progress, not perfection.",
    "Just showing up matters.",
    "Be so good they can’t ignore you.",
    "Discipline is doing it even when you don't feel like it.",
    "Hard work beats talent when talent doesn't work hard.",
    "Crawl if you must, but keep moving forward.",
    "Every commit counts toward greatness."
]

# 💬 Commit messages
commit_messages = [
    "🚀 Boosting productivity with code magic!",
    "🌈 Painting the contribution graph today",
    "💡 A bright idea strikes again!",
    "🧠 Just thinking in Python",
    "🔥 Staying consistent is key",
    "🤖 One more commit for the bot!",
    "📚 Learning something new today",
    "📝 Daily dose of code",
    "📊 Keeping the graph alive",
    "✨ One step at a time",
    "🔧 Fixing the force of habit",
    "🔁 Commit, push, repeat!",
    "🔒 Securing consistency with commits",
    "🎯 Focused commit for focused goals",
    "🛠️ Tinkering toward excellence"
]

target_files = ["daily_log.txt", "progress.md", "inspiration.txt"]

# 🕒 Use IST timezone
ist = pytz.timezone('Asia/Kolkata')
now = datetime.datetime.now(ist)
weekday = now.weekday()
if weekday == 6:
    print("🛌 Sunday! Skipping commits.")
    exit()

# 📅 Date and time formatting
date_key = now.strftime('%Y-%m-%d')
timestamp = now.strftime('%Y-%m-%d %I:%M:%S %p')  # 12-hour format with AM/PM

# 📊 Daily commit tracker
counter_file = ".commit_tracker.json"
min_total = 6
max_total = 14

# Load or create tracker file
if os.path.exists(counter_file):
    with open(counter_file, "r") as f:
        data = json.load(f)
else:
    data = {}

done = data.get(date_key, 0)
remaining = max_total - done

if remaining <= 0:
    print("✅ Max commits reached for today.")
    exit()

# 🎲 Choose 1–5 commits for this time slot
slot_commit = random.randint(1, 5)
slot_commit = min(slot_commit, remaining)

# 📈 Enforce minimum by end of day (last slot effect)
if done + slot_commit < min_total and remaining <= 5:
    slot_commit = min(min_total - done, remaining)

log_entries = []

# 🔁 Make commits
for _ in range(slot_commit):
    quote = random.choice(quotes)
    message = random.choice(commit_messages)
    file = random.choice(target_files)

    with open(file, "a") as f:
        f.write(f"[{timestamp}] {quote}\n")

    subprocess.run(["git", "add", file])
    subprocess.run(["git", "commit", "-m", message])
    log_entries.append(f"[{timestamp}] - {message}")

# Update commit tracker
data[date_key] = done + slot_commit
with open(counter_file, "w") as f:
    json.dump(data, f)

# Append to commit_log
if slot_commit > 0:
    with open("commit_log.txt", "a") as log:
        log.write(f"[{timestamp}] +{slot_commit} commit(s)\n")
        log.write("\n".join(log_entries) + "\n\n")

print(f"✅ {slot_commit} commit(s) made at {timestamp}. Total today: {done + slot_commit}")
