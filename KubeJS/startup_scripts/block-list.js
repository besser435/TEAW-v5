// This will be a common place to put all items. 
// Will be used on the server to disable recipes and loot tables, and used on the client to hide items in the recipe viewers.

// TODO: test that invalid items and tags don't cause problems.
// Should probably also do the validation here, instead of try catch blocks everywhere else.
global.BLOCKED_ITEMS = [
    'minecraft:end_crystal',

    'exposure:interplanar_projector',

    'ironchest:crystal_chest',
    'ironchest:trapped_crystal_chest',
    'ironchest:diamond_to_crystal_chest_upgrade',

    '#refinedstorage:constructors',
    '#refinedstorage:destructors'
]