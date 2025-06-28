import os
import random
import datetime
import subprocess
import json

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

today = datetime.datetime.now()
weekday = today.weekday()
if weekday >= 5:
    print("Weekend! Skipping...")
    exit()

# Track total daily commits across time slots
counter_file = ".commit_tracker.json"
min_total = 4
max_total = 10

# Load or init tracker
if os.path.exists(counter_file):
    with open(counter_file, "r") as f:
        data = json.load(f)
else:
    data = {}

today_str = today.strftime('%Y-%m-%d')
done = data.get(today_str, 0)
remaining = max_total - done
if remaining <= 0:
    print("Reached max commits for today. Exiting.")
    exit()

# Each slot does 0–4 commits, depending on remaining
slot_commit = random.choices([0, 1, 2, 3, 4], weights=[10, 20, 30, 20, 20])[0]
slot_commit = min(slot_commit, remaining)

# Ensure we hit minimum by end of day
if done + slot_commit < min_total and remaining <= 4:
    slot_commit = min(min_total - done, remaining)

log_entries = []

for _ in range(slot_commit):
    quote = random.choice(quotes)
    message = random.choice(commit_messages)
    filename = random.choice(target_files)

    with open(filename, "a") as f:
        f.write(f"{today_str}: {quote}\n")

    subprocess.run(["git", "add", filename])
    subprocess.run(["git", "commit", "-m", message])
    log_entries.append(f" - {message}")

# Save tracker
data[today_str] = done + slot_commit
with open(counter_file, "w") as f:
    json.dump(data, f)

# Append to commit_log.txt
if slot_commit > 0:
    with open("commit_log.txt", "a") as log:
        log.write(f"[{today_str}] +{slot_commit} commits\n")
        log.write("\n".join(log_entries) + "\n\n")
