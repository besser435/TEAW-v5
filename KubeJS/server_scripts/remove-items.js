console.info('TEAW v5 KubeJS server script loaded')

// -- Helpers --
// TODO: This should be precomputed for performance. Just put everything into a list. at server startup/reload.
// Redoing the entire list each time is bad. 

function getAllTargets() {
    let items = [];

    global.BLOCKED_ITEMS.forEach(entry => {
        if (entry.startsWith('#')) {    // Expand tags
            Ingredient.of(entry).itemIds.forEach(id => {
                items.push(id);
            });
        } else {
            items.push(entry);
        }
    });

    return items;
}

// -- Remove recipes --
ServerEvents.recipes(event => {
    let targets = getAllTargets();

    targets.forEach(id => {
        event.remove({ output: id });
        // Intentionally not removing recipes where item is an input,
        // so we notice the problem so we can fix it.
    });
});

// TODO: test me and see if this works and doesnt break anything. The tables should be unchanged, only having the 
// items to be removed, removed. 
// -- Remove from loot tables --
ServerEvents.genericLootTables(event => {
    let targets = getAllTargets();

    event.modifyAllTables(table => {
        table.removePool(pool => {
            pool.entries = pool.entries.filter(entry => {
                return !targets.includes(entry.item);
            });
        });
    });
});




// NOTE The following is probably slow as it runs often and the list is recomputed each time (fix soon). 
// These also probably aren't needed give that the recipes and loot tables are disabled.
// Would also be bad for creative mode if people want to try out the items.
// These have also not been tested. 

// -- Delete on player pickup --
// PlayerEvents.itemPickup(event => {
//     let targets = getAllTargets();

//     if (targets.includes(event.item.id)) {
//         event.item.count = 0;
//     }
// });

// // -- Delete on player craft -- 
// PlayerEvents.crafted(event => {
//     let targets = getAllTargets();

//     if (targets.includes(event.item.id)) {
//         event.item.count = 0;
//     }
// });

// // -- Delete on inventory click --
// PlayerEvents.inventoryChanged(event => {
//     let targets = getAllTargets();

//     event.inventory.allItems.forEach(stack => {
//         if (targets.includes(stack.id)) {
//             stack.count = 0;
//         }
//     });
// });
