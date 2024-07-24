import subprocess
import os
from datetime import datetime, timedelta

# ---------- CONFIG ----------
start_date = datetime(2024, 7, 24, 10, 0, 0)   # 3rd July 2024
end_date = datetime(2024, 8, 15, 10, 0, 0)    # 4th Nov 2024
commits_per_day = 1                           # 15 commits/day
# ----------------------------

total_days = (end_date - start_date).days + 2
print(f"Generating {commits_per_day} commits/day from {start_date.date()} to {end_date.date()} ({total_days} days)")

for day in range(total_days):
    day_base = start_date + timedelta(days=day)
    
    # Collect all file changes for the day in one go
    with open("tmp.txt", "a") as f:
        for c in range(commits_per_day):
            commit_time = day_base + timedelta(minutes=c)
            iso_date = commit_time.strftime("%Y-%m-%dT%H:%M:%S")
            f.write(f"Fake commit {day}-{c} on {iso_date}\n")
    
    # Stage all changes for the day
    subprocess.run(["git", "add", "."], check=True)
    
    # Commit each commit for the day with separate timestamps
    for c in range(commits_per_day):
        commit_time = day_base + timedelta(minutes=c)
        iso_date = commit_time.strftime("%Y-%m-%dT%H:%M:%S")
        commit_msg = f"Fake commit {day}-{c} on {iso_date}"
        
        env = os.environ.copy()
        env["GIT_AUTHOR_DATE"] = iso_date
        env["GIT_COMMITTER_DATE"] = iso_date
        subprocess.run(["git", "commit", "--allow-empty", "-m", commit_msg], env=env, check=True)

print("✅ Done! 15 commits/day from 3rd July to 4th Nov 2024 created.")
print("💡 Push to GitHub with: git push origin main")
