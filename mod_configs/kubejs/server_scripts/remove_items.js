// -- Remove recipes (output only) --
ServerEvents.recipes(event => {
    let validated = [];

    global.RAW_BLOCKED_ITEMS.forEach(entry => {
        if (entry.startsWith('#') || Item.exists(entry)) {
            validated.push(entry);
        }
    });

    // Remove recipes (output only)
    validated.forEach(id => {
        event.remove({ output: id });
    });
});


// -- Remove from loot tables --
LootJS.modifiers(event => {
    let safeLootList = global.RAW_BLOCKED_ITEMS.filter(entry => {
        if (entry.startsWith('#')) return true; // Tags are generally safe to pass
        return Item.exists(entry);              // Only include items that are actually loaded
    });

    if (safeLootList.length > 0) {
        event.addTableModifier(/.*/)
            .removeLoot(Ingredient.of(safeLootList));
            
        if (global.DEV_MODE) {
            console.info(`Removed ${safeLootList.length} loot table entries.`);
        }
    }
});
