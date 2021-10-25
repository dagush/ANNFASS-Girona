DIRT = ['undetermined','vehicle','planttree','furniture','groundgrass','road','entrancegate','lanternlamp',
		'n','CarpetLoopPattern','MetalRusted','tanpaint']
WALL = ['wall','Wall','StoneMasonryMulti','BrickRoughDark','material','Material','whitesample','mktstside',
		'trianglebldg','frontsttotal','shortstlowerfull','cornice','undercornice','slantsectionmktstr',
		'rrtracksideupper','upperbroadside','upperfrontst','triangleend']
WINDOW = ['window','WindowFrameColonial','WindowFrame','WindowFrameModernist','rrtrackbroadside',
		'americathebeautiful','annexfront']
DOOR = ['door','DoorFrame','DoorWayEclectism','DoorFrameModernist','sidedoors','annexbackdoor','frontdoors',
		'vericalpiece','crosspiece']
ROOF = ['roof','Roof','rossroofshot','roofshack','RoofingSlateRounded','RoofingSlateDark','GoogleEarthSnapshot']
STAIRS = ['stairs','Stair']
COLUMN = ['column','Column','archbay','ArchBayOttoman']
OTHER = ['other','railing_baluster','towersteeple','beamframe','pond_pool','balconypatio','parapetmerlon',
		'buttress','dormer','arch','awning',
		'CladdingStuccoWhite']
FLOOR = ['floor','Floor','corridorpath']
CHIMNEY = ['chimney']
CEILING = ['ceiling']
FENCE = ['fence','FencingWoodOld','FencingWeathered']
GARAGE = ['garage']
DOME = ['dome']
ARCHBAY = []
TOWER = ['tower','TowerColonial']
RAILING = ['railing','RailingModernist','railingsection','Railing']
SHUTTER = ['shutter','shutters','ShuttersModernist']
COSA = []


MATERIALS = [WALL,WINDOW,DOOR,ROOF,STAIRS,COLUMN,OTHER,DIRT,FLOOR,CHIMNEY,
			CEILING,FENCE,GARAGE,DOME,ARCHBAY,TOWER,RAILING,SHUTTER,COSA]

def GET_MATERIAL(path):
	for material in MATERIALS:
		if path in material:
			return material[0]
			
	return "[NOT FOUND]"+path
	
	
def GET_CODE(path):
	for material in MATERIALS:
		if path in material:
			return MATERIALS.index(material)
			
	return "[NOT FOUND]"+path

