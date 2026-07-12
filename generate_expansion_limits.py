import sys
from areas import AREAS, BANNED_IN_AREAS

OUTPUT_FILE = "expansion_limits.txt"

def generate_area_ban_script():
    output = []
    output.append("    ;limiter")
    output.append("    console_command add_money seleucid, 2")
    output.append("    monitor_event NewTurnStart TrueCondition")
    for area, settlements in AREAS.items():
        banned_factions = BANNED_IN_AREAS.get(area, [])
        if not banned_factions:
            continue
        for settlement in settlements:
            for faction in banned_factions:
                output.append(f"        if I_SettlementOwner {settlement} = {faction}")
                output.append(f"            console_command sudo capture_settlement {settlement} slave")
                output.append(f"            console_command create_unit {settlement} \"barb infantry slave\" 5 5 5 5")
                output.append("        end_if")
    output.append("    end_monitor")
    output.append("    ;limiter end")
    return "\n".join(output)

if __name__ == "__main__":
    with open(OUTPUT_FILE, "w") as f:
        f.write(generate_area_ban_script())
    print("Done")
