// TODO: should probably just make a validated list instead of checking each time.
// Would run faster, and then we don't need the try catch block everywhere. 
RecipeViewerEvents.removeEntries('item', event => {
	if (!global.DEV_MODE) {
		event.remove(global.BLOCKED_ITEMS);
	}
});

RecipeViewerEvents.addInformation('item', event => {
	event.add('playerplushies:player_plushie', [
		'plushies :3'
	])
})


console.info('TEAW v5 KubeJS client script loaded!')
