#!/usr/bin/env python3
from pathlib import Path

def main():
    current_dir = Path(__file__).resolve().parent
    handoff_path = current_dir / "05-kai-handoff.md"
    script_path = current_dir / "inject-schema.py"

    if not handoff_path.exists() or not script_path.exists():
        print("Required files do not exist.")
        return

    script_content = script_path.read_text(encoding="utf-8")
    handoff_content = handoff_path.read_text(encoding="utf-8")

    # Find the python block
    parts = handoff_content.split("```python")
    if len(parts) >= 2:
        subparts = parts[1].split("```")
        # Replace the first code block's content
        subparts[0] = "\n" + script_content
        parts[1] = "```".join(subparts)
        new_content = "```python".join(parts)
        
        handoff_path.write_text(new_content, encoding="utf-8")
        print("Successfully updated 05-kai-handoff.md with the latest inject-schema.py code!")
    else:
        print("Could not find ```python code block in 05-kai-handoff.md")

if __name__ == "__main__":
    main()
