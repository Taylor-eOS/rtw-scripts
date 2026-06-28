from collections import defaultdict
from itertools import combinations

"""Parses descr_regions format. Groups regions by shared AoR tags so that AoR pools can be identified.
The tag line is the comma-separated line in each block.
Output shows each tag with all settlements that carry it, then for every pair of tags all regions that carry both."""

INPUT_FILE = "descr_regions.txt"
OUTPUT_FILE = "regions_tag_output.txt"

state = {
    "tag_to_regions": defaultdict(list),
    "tag_to_settlements": defaultdict(list),
    "region_to_tags": {},
    "tagpair_to_regions": defaultdict(list),
}

with open(INPUT_FILE, encoding="utf-8") as f:
    lines = [line.strip() for line in f]

block = []
for line in lines + [""]:
    if line:
        block.append(line)
    elif block:
        region = block[0]
        settlement = block[1] if len(block) > 1 else None
        tag_line = next((l for l in block if "," in l), None)
        tags = tuple(sorted(t.strip() for t in tag_line.split(","))) if tag_line else ()
        state["region_to_tags"][region] = tags
        for tag in tags:
            state["tag_to_regions"][tag].append(region)
            if settlement:
                state["tag_to_settlements"][tag].append(settlement)
        for pair in combinations(tags, 2):
            state["tagpair_to_regions"][pair].append(region)
        block = []

with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
    out.write("=== TAG -> SETTLEMENTS ===\n\n")
    for tag in sorted(state["tag_to_settlements"]):
        settlements = sorted(state["tag_to_settlements"][tag])
        quoted = ", ".join(f'"{s}"' for s in settlements)
        out.write(f'    "{tag}": [{quoted}],\n')
    out.write("\n=== SHARED TAG PAIRS (AoR POOLS) ===\n\n")
    for pair in sorted(state["tagpair_to_regions"], key=lambda p: (-len(state["tagpair_to_regions"][p]), p)):
        regions = sorted(state["tagpair_to_regions"][pair])
        out.write(f"[{len(regions)} regions] {pair[0]}, {pair[1]}:\n")
        for r in regions:
            out.write(f"    {r}\n")
        out.write("\n")
    print("Done")
