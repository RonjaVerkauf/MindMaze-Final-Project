"""Collects gameplay events and can export CSV and a simple mood plot."""
from datetime import datetime
import csv, os

class Telemetry:
    def __init__(self):
        self.events = []

    def log(self, **kwargs):
        rec = {"ts": datetime.now().isoformat(timespec="seconds")}
        rec.update(kwargs)
        self.events.append(rec)

    def export_csv(self, path="reports/session_timeline.csv"):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if not self.events:
            return

        # Union aller Keys über alle Events (stabile Reihenfolge)
        all_keys = []
        seen = set()
        for e in self.events:
            for k in e.keys():
                if k not in seen:
                    seen.add(k)
                    all_keys.append(k)

        preferred = [k for k in ("ts", "room", "event", "input", "correct", "mood_score", "mood_state") if k in seen]
        others = [k for k in all_keys if k not in preferred]
        fieldnames = preferred + others

        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            w.writeheader()
            for e in self.events:
                w.writerow({k: e.get(k, "") for k in fieldnames})
    def export_mood_plot(self, path="reports/mood_timeline.png"):
        """Save a simple line plot of mood_score over event index."""
        os.makedirs(os.path.dirname(path), exist_ok=True)

        xs, ys = [], []
        for i, e in enumerate(self.events):
            if "mood_score" in e:
                xs.append(i)
                ys.append(float(e["mood_score"]))
        if not ys:
            return  # nichts zu plotten

        # Headless-Backend und Plot
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        plt.figure()
        plt.plot(xs, ys, marker="o")
        plt.title("Mood score over time")
        plt.xlabel("Event #")
        plt.ylabel("Mood score")
        plt.grid(True, alpha=0.3)
        plt.savefig(path, bbox_inches="tight")
        plt.close()
