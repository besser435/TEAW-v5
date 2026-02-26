# Datapack for TEAW v5
For datapack formatting help, see the default Minecraft datapack in the client jar file.

[Datapack Folder Structure](https://minecraft.wiki/w/Data_pack#Folder_structure)

There is a helper [Python script](format_json.py) to format the JSON files so they are easier to read.

## Added features
* Piglins do not get converted to zombified piglins in the overworld, allowing players 
to [barter](https://minecraft.wiki/w/Bartering#Items_bartered) with them.
* Players will drop their head when they die
* Moss is mineable with a pickaxe and shovel, in addition to the hoe.
* Happy ghasts are faster when a player is on them.


## Mod notes
* The Exposure mod has the inter-planar projector disabled. Ensure this is still valid for v5.
* Create has some nether recipes such as the Blaze burner.


## Recipes are required for the following:
* Nether stuff
* End stuff
* Things that were added after 1.21.4, as the world was made for 1.21.4.
* Things that can be found in structures should not be added. The map maker, CannonMan, can customize the map. 
We should ask him to make a version of the world that doesn't have ruined portals or strongholds, but has things like trial chambers and deep dark biomes.



## Recipe notes
* The old v4 datapack had some recipes that were not needed due to Create mod alternatives. Ensure that there are no duplicates,
as the custom recipes do not feel as nice.

* In the v4 pack, there were some recipes that had NBT data. Use components instead.

* Follow proper convention. Names such as "minecraft" or "create" will override those defaults. If we want to add a new 
feature in addition to the base behavior, it should be under some "teaw" identifier.

* The TEAW recipes are sorted in separate identifiers such as "teaw_nether_recipe" for nether recipes for example.

* Get creative with recipes. Do not just use boring shaped crafting, for everything. Use things like smelting, stonecutting, and smithing.

* Items that can technically be found but are super rare, such as Swift Sneak books, should be craftable. This is so players don't have to spend days
searching already looted structures for something.

## WIP recipe notes
# Should maybe just make make a *complete* list of items before starting on recipes. Don't try to port over old datapack, start from scratch.

* See un-craftable patterns here https://minecraft.wiki/w/Banner_Pattern

