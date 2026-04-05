console.info('TEAW v5 KubeJS client script loaded')

const STUFF = [
	'minecraft:end_crystal',
	'minecraft:diamond',
	'#minecraft:planks'
]


RecipeViewerEvents.removeEntries('item', event => {
	event.remove(STUFF);
})

RecipeViewerEvents.addInformation('item', event => {
	event.add('playerplushies:player_plushie', [
		'plushies :3'
	])
})
