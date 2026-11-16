import os
import json

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def convert_recipe(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, dict):
            return False

        if data.get("type") != "minecraft:crafting_shapeless":
            return False

        changed = False

        # Convert ingredients
        ingredients = data.get("ingredients", [])

        for i, ingredient in enumerate(ingredients):
            if isinstance(ingredient, str):
                if ingredient.startswith("#"):
                    ingredients[i] = {
                        "tag": ingredient[1:]
                    }
                else:
                    ingredients[i] = {
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

    print(f"Converted {count} shapeless crafting recipes.")


main()