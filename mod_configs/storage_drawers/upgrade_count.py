# General storage configuration
BASE_STACK_STORAGE = 1
UPGRADE_SLOTS = 7
STACK_SIZE = 64

# Storage upgrade configuration (from mod config)
upgrades = {
    #"Obsidian":  {"multiplier": 2},
    "Copper":    {"multiplier": 4},     # default: 4
    "Iron":      {"multiplier": 8},     # default: 8
    "Gold":      {"multiplier": 16},    # default: 16
    "Emerald":   {"multiplier": 32},    # default: 64
    "Diamond":   {"multiplier": 64},   # default: 256
    "Netherite": {"multiplier": 128},  # default: 2048
}

# Drawer capacities (unitsPerSlot from mod config)
drawers = {
    "Full Storage 1x1": 32,
    #"Full Storage 1x2": 16,
    "Full Storage 2x2": 8,
    #"Full Compacting":  32,

    #"Half Storage 1x1": 16,
    #"Half Storage 1x2": 8,
    #"Half Storage 2x2": 4,
    #"Half Compacting":  16,
}

for upgrade_name, data in upgrades.items():
    multiplier = data["multiplier"]
    total_multiplier = multiplier * UPGRADE_SLOTS

    print(f"\n======= {upgrade_name} Upgrade (x{multiplier}) =======")
    print(f"Combined upgrade multiplier: {total_multiplier:,}x")

    for drawer_name, units_per_slot in drawers.items():
        max_stacks = (
            units_per_slot
            * BASE_STACK_STORAGE
            * total_multiplier
        )

        max_items = max_stacks * STACK_SIZE

        print(f"{drawer_name}: {max_items:,} items per slot")