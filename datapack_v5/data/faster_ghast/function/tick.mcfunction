# Fast speed when player is near
execute as @e[type=minecraft:happy_ghast] at @s if entity @a[distance=..5] run attribute @s minecraft:flying_speed base set 0.1
# Normal speed when player is not near, so it doesnt float away
execute as @e[type=minecraft:happy_ghast] at @s unless entity @a[distance=..5] run attribute @s minecraft:flying_speed base set 0.05
