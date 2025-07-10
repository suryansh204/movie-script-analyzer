import re
import sys, os
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
from analysis.sentiment import analyze_dialogues


def load_script(filename):
    with open(filename, 'r', encoding="utf-8") as f:
        return f.read()  #All text as one string 
    

def split_scenes(script_text):
    # This pattern finds places in the text where a scene starts ("INT." or "EXT.")
    scene_regex = r"(?=(INT\.|EXT\.).+)"
    
    # re.split cuts the big text into parts at each scene start
    parts = re.split(scene_regex, script_text)

    scenes = []
    # parts list looks like: ['', 'INT. HOUSE - NIGHT\n<dialogue>', 'EXT. PARK - DAY\n<dialogue>', ...]

    for i in range(1, len(parts), 2):
        header = parts[i].strip()            # e.g. "INT. HOUSE - NIGHT"
        body = parts[i + 1].strip() if i+1 < len(parts) else ""
        # Combine header and body back together as one scene
        scenes.append(header + "\n" + body)

    print(f"Found {len(scenes)} scenes.")
    return scenes


def character_line(line):
    if line.startswith(("INT.", "EXT.")):
        return False
    else:
        return line.strip().isupper() and 3 <= len(line.strip()) <= 25

def parse_scene(scene_text):
    lines = scene_text.split("\n")  # Break the scene into individual lines
    dialogues = []
    current_character = None

    for line in lines:
        # If this line looks like a character name, remember it
        if character_line(line):
            current_character = line.strip()
        # Otherwise, if we have a character stored and this line has text,
        # treat it as that character’s dialogue
        elif current_character and line.strip():
            dialogues.append({
                "character": current_character,
                "line": line.strip()
            })
            current_character = None 

    return dialogues


if __name__ == "__main__":
    script = load_script("../data/PulpFiction.txt")
    scenes = split_scenes(script)

    first_scene = scenes[0]
   

    for idx, scene in enumerate(scenes, start=1):
        parsed = parse_scene(first_scene)
        scored = analyze_dialogues(parsed)
        print(f"\nScene {idx} sample:")
        for entry in scored[:3]:
            print(entry)
        
    
    