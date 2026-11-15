# Various mob changes that need to be checked every tick. For performance reasons, they are in separate functions.


# --- Piglin Overworld Zombification Immunity ---
execute as @e[type=minecraft:piglin, tag=!teawZombProcessed] run function teaw_mob_changes:init_piglin


# --- Happy Ghast Speed ---
#execute as @e[type=minecraft:happy_ghast, tag=!teawHappyGhastFast] at @s if entity @a[distance=..5] run function teaw_mob_changes:ghast_set_fast
#execute as @e[type=minecraft:happy_ghast, tag=teawHappyGhastFast] at @s unless entity @a[distance=..5] run function teaw_mob_changes:ghast_set_normal
