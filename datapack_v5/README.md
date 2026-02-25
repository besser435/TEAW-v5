# Datapack for TEAW v5
For datapack formatting help, see the default Minecraft datapack in the client jar file.

[Datapack Folder Structure](https://minecraft.wiki/w/Data_pack#Folder_structure)

There is a helper [Python script](format_json.py) to format the JSON files so they are easier to read.

## Recipes are required for the following:
* Nether stuff
* End stuff
* Things that were added after 1.21.4, as the world was made for 1.21.4.


## Recipe notes
* The old v4 datapack had some recipes that were not needed due to Create mod alternatives. Ensure that there are no duplicates,
as the custom recipes do not feel as nice.

* In the v4 pack, there were some recipes that had NBT data. Use components instead.

* Follow proper convention. Names such as "minecraft" or "create" will override those defaults. If we want to add a new feature in addition to the base behavior, it should be under some "teaw" identifier.

* The TEAW recipes are sorted in separate identifiers such as "teaw_nether_recipe" for nether recipes for example.


## Added features
* Players will drop their head when they die
* Moss is mineable with a pickaxe and shovel, in addition to the hoe.


## Mod notes
* The Exposure mod has the inter-planar projector disabled. Ensure this is still valid for v5.
* Create has some nether recipes such as the Blaze burner.