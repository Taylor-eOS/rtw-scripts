import os
import sys

descr_regions_path = "descr_regions.txt"
regions_list_path = "regions_plain.txt"
output_path = "settlements_list.txt"

def load_descr_lines(path):
    if not os.path.exists(path):
        print(f"Error: {path} not found.")
        sys.exit(1)
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        lines = [line.strip() for line in f]
    valid_lines = []
    for line in lines:
        cleaned = "".join(c for c in line if ord(c) != 160).strip()
        if cleaned and not cleaned.startswith(";"):
            valid_lines.append(cleaned)
    return valid_lines

def load_input_regions(regions_list_path):
    if not os.path.exists(regions_list_path):
        print(f"Error: {regions_list_path} not found.")
        sys.exit(1)
    with open(regions_list_path, "r", encoding="utf-8") as f:
        items = []
        for line in f:
            cleaned = "".join(c for c in line if ord(c) != 160).strip()
            if cleaned and not cleaned.startswith(";"):
                items.append(cleaned)
    return items

def find_settlement(region_name, descr_lines):
    for i, line in enumerate(descr_lines):
        if line == region_name and i + 1 < len(descr_lines):
            return descr_lines[i + 1]
    return None

def convert_regions_to_settlements():
    descr_lines = load_descr_lines(descr_regions_path)
    input_items = load_input_regions(regions_list_path)
    output_lines = []
    missing_items = []
    for item in input_items:
        settlement = find_settlement(item, descr_lines)
        if settlement is not None:
            output_lines.append(settlement)
        else:
            missing_items.append(item)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines) + "\n")
    print(f"Conversion complete. Output written to {output_path}")
    if missing_items:
        print("[WARNING] The following regions were not found in descr_regions.txt:")
        for item in missing_items:
            print(f"  - '{item}'")
    else:
        print("All regions successfully matched to their respective settlements.")

if __name__ == "__main__":
    convert_regions_to_settlements()
