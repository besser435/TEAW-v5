console.info('TEAW v5 KubeJS client script loaded')

// TODO: should probably just make a validated list instead of checking each time.
// Would run faster, and then we need the try catch block everywhere. 
RecipeViewerEvents.removeEntries('item', event => {
	global.BLOCKED_ITEMS.forEach(entry => {
		try {
			event.remove(entry);
		} catch (err) {
			console.warn(`Invalid entry: ${entry}`);
		}
	});
});

RecipeViewerEvents.addInformation('item', event => {
	event.add('playerplushies:player_plushie', [
		'plushies :3'
	])
})
