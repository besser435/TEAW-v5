# Upgrade configuration
upgrades = {
    "Obsidian":     {"enabled": False, "multiplier": 2},
    "Copper":       {"enabled": True, "multiplier": 4},
    "Iron":         {"enabled": True, "multiplier": 4},
    "Gold":         {"enabled": True, "multiplier": 8},
    "Emerald":      {"enabled": True, "multiplier": 16},
    "Diamond":      {"enabled": True, "multiplier": 64},
    "Netherite":    {"enabled": True, "multiplier": 128},
}

# Drawer base capacities (in stacks)
drawers = {
    "1x1": 32,
    "2x2": 8#,
    #"Compacting": 32
}

UPGRADE_SLOTS = 7
STACK_SIZE = 64

for upgrade_name, data in upgrades.items():
    if not data["enabled"]:
        continue

    multiplier = data["multiplier"]
    total_multiplier = multiplier * UPGRADE_SLOTS

    print(f"======= {upgrade_name} Upgrade (x{multiplier}) =======")

    for drawer_name, base_stacks in drawers.items():
        max_stacks = base_stacks * total_multiplier
        max_items = max_stacks * STACK_SIZE

        print(f"{drawer_name} Drawer max items: {max_items:,}")
