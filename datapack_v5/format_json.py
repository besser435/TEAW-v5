import json
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

DIRECTORY = "data"

def format_json_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        print(f"Formatted: {filepath}")

    except Exception as e:
        print(f"Skipped {filepath}: {e}")


def main():
    for root, dirs, files in os.walk(DIRECTORY):
        for file in files:
            if file.endswith(".json"):
                format_json_file(os.path.join(root, file))


if __name__ == "__main__":
    main()