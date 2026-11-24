// TODO: should probably just make a validated list instead of checking each time.
// Would run faster, and then we don't need the try catch block everywhere. 
RecipeViewerEvents.removeEntries('item', event => {
    let toHide = global.RAW_BLOCKED_ITEMS.filter(entry => {
        if (entry.startsWith('#')) return true;
        return Item.exists(entry);
    });

    event.remove(toHide);
});

// RecipeViewerEvents.addInformation('item', event => {
// 	event.add('playerplushies:player_plushie', [
// 		'plushies :3'
// 	])
// })
