import os
import json

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def convert_recipe(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, dict):
            return False

        if data.get("type") != "minecraft:crafting_shaped":
            return False

        changed = False

        # Convert key ingredients
        key = data.get("key", {})

        for symbol, ingredient in key.items():
            if isinstance(ingredient, str):
                if ingredient.startswith("#"):
                    key[symbol] = {
                        "tag": ingredient[1:]
                    }
                else:
                    key[symbol] = {
                        "item": ingredient
                    }

                changed = True

        # Ensure result has a count
        result = data.get("result")

        if isinstance(result, dict) and "count" not in result:
            result["count"] = 1
            changed = True

        if changed:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            return True

        return False

    except Exception as e:
        print(f"ERROR {filepath}: {e}")
        return False


def main():
    count = 0

    for root, dirs, files in os.walk("."):
        for file in files:
            if not file.endswith(".json"):
                continue

            filepath = os.path.join(root, file)

            if convert_recipe(filepath):
                count += 1

    print(f"Converted {count} shaped crafting recipes.")


main()