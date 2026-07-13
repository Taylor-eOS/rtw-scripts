input_filename = "export_descr_unit.txt"
output_filename = "output.txt"
FACTION = "slave"

def main():
    with open(input_filename, "r", encoding="utf-8") as f:
        lines = f.readlines()
    unit_type = None
    faction_units = []
    for raw_line in lines:
        line = raw_line.strip()
        if not line or line.startswith(";"):
            if not line:
                unit_type = None
            continue
        if line.startswith("type"):
            unit_type = line[len("type"):].strip()
        elif line.startswith("ownership"):
            factions = [f.strip() for f in line[len("ownership"):].strip().split(",")]
            if unit_type is not None and FACTION in factions:
                faction_units.append(unit_type)
            unit_type = None
    with open(output_filename, "w", encoding="utf-8") as f:
        for name in faction_units:
            f.write(name + "\n")

if __name__ == "__main__":
    main()
    print("Done")
