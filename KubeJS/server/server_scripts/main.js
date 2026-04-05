console.info('TEAW v5 KubeJS server script loaded')

// -- Helpers --
// TODO: This should be precomputed for performance. Just put everything into a list. at server startup/reload.
// Redoing the entire list each time is bad. 
function getAllTargets(event) {
    let items = [];

    // Direct items
    REMOVED.items.forEach(id => {
        items.push(id);
    });

    // Tags → expand into items
    REMOVED.tags.forEach(tag => {
        Ingredient.of(`#${tag}`).itemIds.forEach(id => {
        items.push(id);
        });
    });

    return items;
}

// -- Remove recipes --
ServerEvents.recipes(event => {
    let targets = getAllTargets(event);

    targets.forEach(id => {
        event.remove({ output: id });
        event.remove({ input: id });
    });
});

// -- Remove from loot tables --
ServerEvents.genericLootTables(event => {
    let targets = getAllTargets(event);

    event.modifyAllTables(table => {
        table.removePool(pool => {
            pool.entries = pool.entries.filter(entry => {
                return !targets.includes(entry.item);
            });
        });
    });
});




// NOTE The following is probably slow as it runs often. 
// These also probably aren't needed give that the recipes and loot tables are disabled.
// Would also be bad for creative mode if people want to try out the items.

// -- Delete on player pickup --
// PlayerEvents.itemPickup(event => {
//     let targets = getAllTargets(event);

//     if (targets.includes(event.item.id)) {
//         event.item.count = 0;
//     }
// });

// // -- Delete on player craft -- 
// PlayerEvents.crafted(event => {
//     let targets = getAllTargets(event);

//     if (targets.includes(event.item.id)) {
//         event.item.count = 0;
//     }
// });

// // -- Delete on inventory click --
// PlayerEvents.inventoryChanged(event => {
//     let targets = getAllTargets(event);

//     event.inventory.allItems.forEach(stack => {
//         if (targets.includes(stack.id)) {
//         stack.count = 0;
//         }
//     });
// });
