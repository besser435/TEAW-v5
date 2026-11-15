import os
import json
os.chdir(os.path.dirname(os.path.abspath(__file__)))

RECIPES_ROOT = "data/teaw_recipes/recipe"
OUTPUT_FILE = "emi.json"

def collect_recipe_ids(root):
    recipe_ids = []

    for dirpath, _, filenames in os.walk(root):
        for file in filenames:
            if not file.endswith(".json"):
                continue

            full_path = os.path.join(dirpath, file)

            # Get path relative to RECIPES_ROOT
            rel_path = os.path.relpath(full_path, root)

            # Remove .json extension
            rel_path = rel_path[:-5]

            # Convert Microslop backslashes to forward slashes
            rel_path = rel_path.replace("\\", "/")

            # Build EMI recipe ID
            recipe_id = f"jei:/teaw_recipes/{rel_path}"

            recipe_ids.append(recipe_id)

    return sorted(recipe_ids)


def generate_emi_file(recipe_ids):
    emi_data = {
        # Commenting out unused sections for now. 
        # EMI seems to remake them if they are not present, while preserving the already existing recipe_defaults.

        #"favorites": [],
        #"lookup_history": [],
        #"craft_history": [],
        "recipe_defaults": {
            "added": recipe_ids #,
            #"tags": {},
            #"resolutions": {},
            #"disabled": []
        } #,
        #"hidden_stacks": []
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(emi_data, f, indent=2)

    print(f"Generated ./{OUTPUT_FILE} with {len(recipe_ids)} recipes.")


#if __name__ == "__main__":
recipes = collect_recipe_ids(RECIPES_ROOT)
generate_emi_file(recipes)
