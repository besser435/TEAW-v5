// -- Remove recipes (output only) --
ServerEvents.recipes(event => {
    global.BLOCKED_ITEMS.forEach(id => {
        event.remove({ output: id });
        // Intentionally not removing recipes where the item is an ingredient,
        // so we notice the problem so we can fix it.
    });
});

//-- Remove from loot tables --
//  FIXME idk if its some other bug, but it blocks stone from dropping when cobblestone is blocked.
// Could be something else though. 
// nvm im stupid, stone drops cobblestone.
LootJS.lootTables(event => {
	event.modifyLootTables(/.*/)
        .removeItem(Ingredient.of(global.BLOCKED_ITEMS));
});

console.info('TEAW v5 KubeJS server script loaded!')
