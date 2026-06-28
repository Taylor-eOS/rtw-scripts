import os
import sys

_STATE = {
    "directory": "",
    "output_directory": "",
    "from_enc": "",
    "to_enc": "",
}

def prompt_user():
    _STATE["directory"] = input("Enter absolute path to the directory: ").strip()
    if not os.path.isabs(_STATE["directory"]) or not os.path.isdir(_STATE["directory"]):
        print("Invalid absolute path or directory does not exist.", file=sys.stderr)
        sys.exit(1)
    print("Select direction of conversion:")
    print("1: UTF-8 to UTF-16LE")
    print("2: UTF-16LE to UTF-8")
    choice = input("Enter conversion option: ").strip()
    if choice == "1":
        _STATE["from_enc"] = "UTF-8"
        _STATE["to_enc"] = "UTF-16LE"
    elif choice == "2":
        _STATE["from_enc"] = "UTF-16LE"
        _STATE["to_enc"] = "UTF-8"
    else:
        print("Invalid choice.", file=sys.stderr)
        sys.exit(1)
    _STATE["output_directory"] = _STATE["directory"].rstrip("/") + "_converted"
    os.makedirs(_STATE["output_directory"], exist_ok=True)

def convert_file(filepath):
    try:
        with open(filepath, "r", encoding=_STATE["from_enc"]) as f_in:
            content = f_in.read()
        out_path = os.path.join(_STATE["output_directory"], os.path.basename(filepath))
        with open(out_path, "w", encoding=_STATE["to_enc"]) as f_out:
            f_out.write(content)
    except Exception as e:
        print(f"Failed to convert {filepath}: {e}", file=sys.stderr)

def convert_directory():
    for filename in os.listdir(_STATE["directory"]):
        filepath = os.path.join(_STATE["directory"], filename)
        if os.path.isfile(filepath):
            convert_file(filepath)

if __name__ == "__main__":
    prompt_user()
    convert_directory()

