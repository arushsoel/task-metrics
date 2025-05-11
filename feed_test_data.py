#!/usr/bin/env python3

import random, time, sys, requests, itertools

URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8080"
tools = ["upgrader", "etl", "ci", "scanner"]
tasks = ["healthchecks", "backup", "sync", "deploy"]
statuses = ["completed", "failed", "succeeded"]

for _ in itertools.count():
    payload = {
        "tool": random.choice(tools),
        "task": random.choice(tasks),
        "status": random.choice(statuses),
        "duration": random.randint(5, 600),
    }
    r = requests.post(f"{URL}/api/tasks", json=payload, timeout=5)
    r.raise_for_status()
    print("Sent", payload)
    time.sleep(2)
