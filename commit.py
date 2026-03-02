import os
import random
import datetime
import subprocess
import json
import pytz  # Timezone support
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
counter_file = os.path.join(BASE_DIR, ".commit_tracker.json")

def perform_commits():

    # 🌿 Expanded inspirational quotes
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
        "Every commit counts toward greatness.",
        "Build something you're proud of.",
        "Bit by bit, you create the masterpiece.",
        "The habit of showing up wins the game.",
        "Don’t break the streak — commit today!",
        "From bugs to brilliance — keep coding!",
        "It’s not about perfection. It’s about progress.",
        "You’re one step closer to your goal.",
        "Keep calm and commit on.",
        "Even a tiny push moves the needle."
    ]

    # 🌈 Expanded commit messages
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
        "🎯 Another mark on the roadmap",
        "✅ Small win for the day",
        "📦 Packaging progress, one file at a time",
        "🔧 Tweaked, tuned, and tightened",
        "🧪 Experimented with improvements",
        "🎉 Progress never looked better",
        "💭 Thoughts turned into code",
        "🛠️ Building habits, one commit at a time",
        "📈 Slow and steady climb",
        "🚧 Another brick in the dev wall"
    ]

    target_files = ["daily_log.txt", "progress.md", "inspiration.txt"]

    # ⏰ IST timezone & 12-hour format

    # Time setup
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.datetime.now(ist)
    weekday = now.weekday()  # Monday = 0, Sunday = 6
    date_key = now.strftime('%Y-%m-%d')
    timestamp = now.strftime('%Y-%m-%d %I:%M:%S %p')

    # Paths
    # counter_file = ".commit_tracker.json"
    min_total = 3
    max_total = 15

    # Load or initialize tracking
    if os.path.exists(counter_file):
        with open(counter_file, "r") as f:
            data = json.load(f)
    else:
        data = {}

    # Track weekly commit days
    def get_week_key(date):
        return date.strftime("%Y-W%U")  # Year-WeekNumber (Monday as first day)

    week_key = get_week_key(now)
    week_data = data.get("week_data", {})
    week_commits = week_data.get(week_key, [])

    # Choose 4 random days (only once per week)
    if len(week_commits) == 0:
        num_days = random.randint(3, 5)  # Commit 3 to 5 days each week
        week_commits = sorted(random.sample(range(7), num_days))
        week_data[week_key] = week_commits
        data["week_data"] = week_data
        with open(counter_file, "w") as f:
            json.dump(data, f)

    # ❌ Skip if today is not one of the selected commit days
    if weekday not in week_commits:
        print(f"🛌 {now.strftime('%A')} not selected for this week. Skipping commits.")
        return # Change exit() to return

    # Daily count
    done = data.get(date_key, 0)
    remaining = max_total - done
    if remaining <= 0:
        print("✅ Max commits reached for today.")
        return # Change exit() to return

    # Random number of commits
    slot_commit = random.randint(1, 5)
    slot_commit = min(slot_commit, remaining)

    # Ensure min_total is met
    if done + slot_commit < min_total and remaining <= 6:
        slot_commit = min(min_total - done, remaining)

    log_entries = []

    # Do the commits
    for _ in range(slot_commit):
        quote = random.choice(quotes)
        message = random.choice(commit_messages)
        filename = random.choice(target_files)

        with open(filename, "a") as f:
            f.write(f"[{timestamp}] {quote}\n")

        subprocess.run(["git", "add", filename])
        subprocess.run(["git", "commit", "-m", message])
        log_entries.append(f"[{timestamp}] - {message}")
    # After the loop finishes all commits for the slot
    subprocess.run(["git", "push"])
    # Update tracking
    data[date_key] = done + slot_commit
    data["week_data"] = week_data
    with open(counter_file, "w") as f:
        json.dump(data, f)

    # Log
    if slot_commit > 0:
        with open("commit_log.txt", "a") as log:
            log.write(f"[{timestamp}] +{slot_commit} commit(s)\n")
            log.write("\n".join(log_entries) + "\n\n")

    print(f"✅ {slot_commit} commit(s) made at {timestamp}. Total today: {done + slot_commit}")

