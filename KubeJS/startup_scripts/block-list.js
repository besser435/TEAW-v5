//priority: 100

/*
If true, this will disable recipe hiding so that we can verify recipes are disabled.
If true, prints the entire blocklist after processing to the console.
*/
global.DEV_MODE = false; 

/*
Place item IDs and tags here to disable recipes, hide items in recipe viewers,
and to prevent players from obtaining them (if the inventory events are enabled).

This file must load before the others. Make sure its name is first alphabetically.
*/
global.RAW_BLOCKED_ITEMS = [
    // Minecraft
    'minecraft:end_crystal',
    'minecraft:totem_of_undying',   // Evokers shouldn't spawn, but just in case

    // Exposure
    'exposure:interplanar_projector',

    // Iron Chests
    'ironchest:crystal_chest',
    'ironchest:trapped_crystal_chest',
    'ironchest:diamond_to_crystal_chest_upgrade',

    // RS interfaces
    '#refinedstorage:constructors',
    '#refinedstorage:destructors',
    'refinedstorage:storage_monitor',
    '#refinedstorage:network_transmitters',
    '#refinedstorage:network_receivers',
    '#refinedstorage:disk_interfaces',
    'refinedstorage:wrench',    // Use Create wrench instead

    // RS autocrafting
    '#refinedstorage:autocrafters',
    '#refinedstorage:autocrafter_managers',
    '#refinedstorage:autocrafting_monitors',
    'refinedstorage:wireless_autocrafting_monitor',
    'refinedstorage:creative_wireless_autocrafting_monitor',
    'refinedstorage:pattern',
    'refinedstorage:autocrafting_upgrade',

    // RS disks
    '#refinedstorage:pattern_grids',
    'refinedstorage:disk_drive',
    'refinedstorage:portable_grid',
    'refinedstorage:creative_portable_grid',

    // RS Storage blocks
    'refinedstorage:1k_storage_block',
    'refinedstorage:4k_storage_block',
    'refinedstorage:16k_storage_block',
    'refinedstorage:64k_storage_block',
    'refinedstorage:creative_storage_block',

    'refinedstorage:64b_fluid_storage_block',
    'refinedstorage:256b_fluid_storage_block',
    'refinedstorage:1024b_fluid_storage_block',
    'refinedstorage:4096b_fluid_storage_block',
    'refinedstorage:creative_fluid_storage_block',

    // RS storage components
    'refinedstorage:1k_storage_part',
    'refinedstorage:4k_storage_part',
    'refinedstorage:16k_storage_part',
    'refinedstorage:64k_storage_part',
    'refinedstorage:storage_housing',

    'refinedstorage:64b_fluid_storage_part',
    'refinedstorage:256b_fluid_storage_part',
    'refinedstorage:1024b_fluid_storage_part',
    'refinedstorage:4096b_fluid_storage_part',

    // RS disks
    '#refinedstorage:storage_disks',
    'refinedstorage:creative_storage_disk',

    '#refinedstorage:fluid_storage_disks',
    'refinedstorage:creative_fluid_storage_disk',

    // RS upgrades
    'refinedstorage:fortune_1_upgrade',
    'refinedstorage:fortune_2_upgrade',
    'refinedstorage:fortune_3_upgrade',
    'refinedstorage:silk_touch_upgrade'
];

