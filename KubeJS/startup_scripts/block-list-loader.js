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
let cleaned = [];

RAW_BLOCKED_ITEMS.forEach(entry => {
    if (entry.startsWith('#')) {
        cleaned.push(entry);
    } else {    // Needed for recipe viewer. Does not like missing items.
        if (Item.exists(entry)) {
            cleaned.push(entry);
        } else {
            console.warn(`[BLOCKED ITEMS] Missing item skipped: ${entry}`);
        }
    }
});

// -- Final structures --
global.BLOCKED_ITEMS = cleaned.filter((item, index) => cleaned.indexOf(item) === index); // Rhino-compatible array

if (global.DEV_MODE) {
    console.info(`[BLOCKED ITEMS] Blocked the following items: ${global.BLOCKED_ITEMS.join(', ')}`);
}

console.info(`[BLOCKED ITEMS] Blocked ${global.BLOCKED_ITEMS.length} items`);
