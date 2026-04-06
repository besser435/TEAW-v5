console.info('TEAW v5 Item Blocklist loader running')

/*
-- Blocked items list --

Place item IDs and tags here to disable recipes, hide items in recipe viewers,
and to prevent players from obtaining them (if the inventory events are enabled).

This file must load before the others. Make sure its name is first alphabetically.
*/
const RAW_BLOCKED_ITEMS = [
    'minecraft:end_crystal',
    'minecraft:cobblestone',

    'exposure:interplanar_projector',

    'ironchest:crystal_chest',
    'ironchest:trapped_crystal_chest',
    'ironchest:diamond_to_crystal_chest_upgrade',

    '#refinedstorage:constructors',
    '#refinedstorage:destructors'
];

/*
If true, this will disable recipe hiding so that we can verify recipes are disabled.
If true, prints the entire blocklist after processing to the console.
*/
global.DEV_MODE = false; 



// -- Processing --
let expanded = [];

RAW_BLOCKED_ITEMS.forEach(entry => {
    if (entry.startsWith('#')) {
        expanded.push(entry);
    } else {
        if (Item.exists(entry)) {
            expanded.push(entry);
        } else {
            console.warn(`[BLOCKED ITEMS] Missing item skipped: ${entry}`);
        }
    }
});

// -- Final structures --
global.BLOCKED_ITEMS = expanded.filter((item, index) => expanded.indexOf(item) === index); // Rhino-compatible array

if (global.DEV_MODE) {
    console.info(`[BLOCKED ITEMS] Blocked ${global.BLOCKED_ITEMS.length} items: ${global.BLOCKED_ITEMS.join(', ')}`);
}
