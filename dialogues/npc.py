import random
# Eternal villager line greeting
eternal_villager_lines = [

    "\nEternal Villager: Ah, traveler… the lands be old, thou knowest. Long ago, there was a man whose smile did hide sharp teeth… they say he vanished into the caverns, but who can tell what be truth?",
    "\nEternal Villager: Some folk come to these parts seeking warmth, yet beware… there be those who charm the weak-hearted, and leave naught but ashes in their wake.",
    "\nEternal Villager: The village whispers of cruel men, though most deem them gone. Yet anon, their shadow doth creep back, clad in kindness, walking amongst us.",
    "\nEternal Villager: I remember a time when fear had a name… they say he hides in plain sight now, watching, waiting, patient as stone.",
    "\nEternal Villager: Legends speak of a man who once ruled through cunning and cruelty. He vanished up the cavern long ago… some say he waits for those brave enough to follow.",
    "\nEternal Villager: Thou shalt find no weapon sharp enough to strike at truth here, traveler… only those who dare see through the smiles of men may endure.",
    "\nEternal Villager: Eternal we be, yet some evils last longer than the oldest oaks. A man once cruel walketh again in the land… and the caverns know his secrets.",
    "\nEternal Villager: Mistake not this village for safety. Even the kindest faces may hide the cruelest pasts… and some tales be whispered only to those who ask.",
    "\nEternal Villager: They say he who hath hurt many now feigneth harmlessness… yet every shadow holdeth a memory, and some forgive never.",
    "\nEternal Villager: I have seen men rise, fall, and vanish… yet one returned, clad as an old man. Those who meet him see the world ne’er the same again."
]
def eternal_villager_ask():
    print(random.choice(eternal_villager_lines))
# Eternal Villagers  tells history of village
eternal_villager_history = [

    "\nEternal Villager: Ah, the Eternal Village… long before this age, it was naught but a whisper in the caverns, tread by only the stout of heart.",
    "\nEternal Villager: Legends tell of kings, wanderers, and knaves who passed through these streets… yet still it endureth, silent and eternal.",
    "\nEternal Villager: They speak of a cruel man who wrought sorrow upon these lands… his shadow lingereth, e’en in peace.",
    "\nEternal Villager: The folk ye see now be but heirs of ancient tales, bearing memories older than the stones beneath thy feet.",
    "\nEternal Villager: Some say the caverns themselves remember the village’s past, murmuring secrets to those who hark with care."
]
def eternal_village():
    print(random.choice(eternal_villager_history))
# Eternal villager says farewell
eternal_villager_farewell = [

    "\nEternal Villager: Fare thee well, traveler… may thy path be free of shadows.",
    "\nEternal Villager: Go with care, and may the stones beneath thy feet guide thee true.",
    "\nEternal Villager: Godspeed, wanderer… the village shall wait for thy return.",
    "\nEternal Villager: May thy courage not falter, and thy blade stay keen.",
    "\nEternal Villager: Safe travels… and keep an eye upon the caverns, lest they watch thee back.",
    "\nEternal Villager: Farewell, friend. The winds shall carry thee where thou needst go.",
    "\nEternal Villager: Go now, and remember: even the smallest spark may light the darkest path.",
    "\nEternal Villager: Part in peace, traveler… but forget not the whispers of this village.",
    "\nEternal Villager: Mayhap we shall meet again before the moon wanes twice.",
    "\nEternal Villager: God’s grace go with thee… and beware those who smile too kindly."
]
def eternal_villager_bye():
    print(random.choice(eternal_villager_farewell))
# Random NPC
npcs = [
    {"name": "Eldrin the Eternal Miner", "type": "Miner"},
    {"name": "Serah of Sustenance", "type": "Cook"},
    {"name": "Azorious the Scout", "type": "Scout"},
    {"name": "Mira the Herbalist", "type": "Healer"},
    {"name": "Baron the Smith", "type": "Blacksmith"},
    {"name": "Ilyra the Acolyte", "type": "Priestess"}
]
# Random npc dialogues  for giving quests
npc_quest_dialogues = [
    "Traveler! A moment of your time—there’s something that needs your blade.",
    "Pardon me, stranger... you look capable. Might you lend your strength?",
    "Ah, a fresh soul in the Eternal Village... perhaps you can aid me.",
    "Please, the Rift has grown restless again. We need help.",
    "You there—yes, you. The glow of courage shines in your eyes.",
]