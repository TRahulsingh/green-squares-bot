import os
import random
import datetime
import subprocess
import json
import pytz  # Added for timezone support

# 🌿 Inspirational quotes and messages
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
    "Just showing up matters."
]

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
    "✨ One step at a time"
]

target_files = ["daily_log.txt", "progress.md", "inspiration.txt"]

# 🕒 Use IST timezone (12-hour format with AM/PM)
ist = pytz.timezone('Asia/Kolkata')
now = datetime.datetime.now(ist)
weekday = now.weekday()
if weekday == 6:  # Sunday only
    print("🛌 Sunday! Skipping commits.")
    exit()

# 📅 Date and Time formatting
date_key = now.strftime('%Y-%m-%d')  # For commit tracking
timestamp = now.strftime('%Y-%m-%d %I:%M:%S %p')  # For logs (12-hour format + AM/PM)

# 🧠 Daily commit tracking
counter_file = ".commit_tracker.json"
min_total = 4
max_total = 10

# 📦 Load or create tracker
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

# 🎲 Choose 1–4 commits
slot_commit = random.choices([1, 2, 3, 4], weights=[25, 30, 25, 20])[0]
slot_commit = min(slot_commit, remaining)

# ⛳ Ensure minimum total by day-end
if done + slot_commit < min_total and remaining <= 4:
    slot_commit = min(min_total - done, remaining)

log_entries = []

# 🔁 Generate commits
for _ in range(slot_commit):
    quote = random.choice(quotes)
    message = random.choice(commit_messages)
    filename = random.choice(target_files)

    # Write timestamped quote to selected file
    with open(filename, "a") as f:
        f.write(f"[{timestamp}] {quote}\n")

    subprocess.run(["git", "add", filename])
    subprocess.run(["git", "commit", "-m", message])
    log_entries.append(f"[{timestamp}] - {message}")

# 📌 Update tracker
data[date_key] = done + slot_commit
with open(counter_file, "w") as f:
    json.dump(data, f)

# 📝 Update commit_log.txt
if slot_commit > 0:
    with open("commit_log.txt", "a") as log:
        log.write(f"[{timestamp}] +{slot_commit} commit(s)\n")
        log.write("\n".join(log_entries) + "\n\n")

# ✅ Final log
print(f"✅ {slot_commit} commit(s) made at {timestamp}. Total today: {done + slot_commit}")
