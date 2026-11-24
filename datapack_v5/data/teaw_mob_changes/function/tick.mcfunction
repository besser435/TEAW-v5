# Various mob changes that need to be checked every tick. For performance reasons, they are in separate functions.


# --- Piglin Overworld Zombification Immunity ---
execute as @e[type=minecraft:piglin, tag=!teawZombProcessed] run function teaw_mob_changes:init_piglin
