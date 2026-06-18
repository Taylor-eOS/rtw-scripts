import os
import sys

descr_regions_path = "descr_regions.txt"
regions_list_path = "regions_plain.txt"
output_path = "settlements_list.txt"

def load_regions_dictionary(descr_regions_path):
    settlement_to_region = {}
    if not os.path.exists(descr_regions_path):
        print(f"Error: {descr_regions_path} not found.")
        sys.exit(1)
    with open(descr_regions_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = [line.strip() for line in f]
    valid_lines = []
    for line in lines:
        cleaned = "".join(c for c in line if ord(c) != 160).strip()
        if cleaned and not cleaned.startswith(";"):
            valid_lines.append(cleaned)
    for i in range(len(valid_lines)):
        parts = valid_lines[i].split()
        if len(parts) == 3 and all(p.isdigit() for p in parts):
            if i >= 4:
                region_name = valid_lines[i - 4]
                settlement_name = valid_lines[i - 3]
                settlement_to_region[settlement_name] = region_name
    return settlement_to_region

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

def convert_regions_to_settlements():
    settlement_map = load_regions_dictionary(descr_regions_path)
    input_items = load_input_regions(regions_list_path)
    output_lines = []
    missing_items = []
    for item in input_items:
        if item in settlement_map:
            output_lines.append(settlement_map[item])
        else:
            missing_items.append(item)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines) + "\n")
    print(f"Conversion complete. Output written to {output_path}")
    if missing_items:
        print("[WARNING] The following settlements were not found in descr_regions.txt:")
        for item in missing_items:
            print(f"  - '{item}'")
    else:
        print("All settlements successfully matched to their respective regions.")

if __name__ == "__main__":
    convert_regions_to_settlements()
