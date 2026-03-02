import json
import os
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_ALLSKY_DIR = os.path.join(ROOT, "static", "allsky")
DATA_ALLSKY_DIR = os.path.join(ROOT, "data", "allsky")
INDEX_PATH = os.path.join(DATA_ALLSKY_DIR, "index.json")


def infer_type(filename: str) -> str:
    name = filename.lower()
    if "startrail" in name or "startrails" in name:
        return "startrails"
    if "meteor" in name or "meteors" in name:
        return "meteors"
    if "timelapse" in name or "video" in name:
        return "timelapse"
    return "allsky"


def main() -> None:
    items = []

    if not os.path.isdir(STATIC_ALLSKY_DIR):
        os.makedirs(STATIC_ALLSKY_DIR, exist_ok=True)

    for year in sorted(os.listdir(STATIC_ALLSKY_DIR)):
        year_path = os.path.join(STATIC_ALLSKY_DIR, year)
        if not os.path.isdir(year_path):
            continue

        for month in sorted(os.listdir(year_path)):
            month_path = os.path.join(year_path, month)
            if not os.path.isdir(month_path):
                continue

            for day in sorted(os.listdir(month_path)):
                day_path = os.path.join(month_path, day)
                if not os.path.isdir(day_path):
                    continue

                # 构造日期字符串，若解析失败则跳过
                try:
                    date_obj = datetime.strptime(f"{year}-{month}-{day}", "%Y-%m-%d")
                    date_str = date_obj.strftime("%Y-%m-%d")
                except ValueError:
                    continue

                for fname in sorted(os.listdir(day_path)):
                    if not fname.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                        continue

                    rel_image = f"allsky/{year}/{month}/{day}/{fname}"
                    items.append(
                        {
                            "date": date_str,
                            "title": fname,
                            "image": rel_image,
                            "type": infer_type(fname),
                            "description": "",
                        }
                    )

    items.sort(key=lambda x: x["date"], reverse=False)

    os.makedirs(DATA_ALLSKY_DIR, exist_ok=True)
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()

