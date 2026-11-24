import os
import zipfile

os.chdir(os.path.dirname(os.path.abspath(__file__)))

pack_name = "teaw_v5_datapack"
output_file = f"{pack_name}.zip"

file_excludes = {".md", ".py", ".zip"}

with zipfile.ZipFile(output_file, "w", zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d != "__pycache__"]

        for file in files:
            if os.path.splitext(file)[1].lower() in file_excludes:
                continue

            filepath = os.path.join(root, file)
            arcname = os.path.relpath(filepath, ".")

            zipf.write(filepath, arcname)

print(f"Built {output_file}")