import random

# Eternal inkeeper greets player
eternal_inkeeper_lines_greet = [

    "Eternal Innkeeper: 'Welcome, traveler. You look weary — rest comes easy within these walls.'",
    "Eternal Innkeeper: 'Ah, another soul finds their way here. The Sanctuary always opens for the worthy.'",
    "Eternal Innkeeper: 'Peace upon you, wanderer. The light of this hall remembers all who seek refuge.'",
    "Eternal Innkeeper: 'Evenin’, traveler. You’ve got that cavern dust all over you — care for a room or a meal?'",
    "Eternal Innkeeper: 'Welcome, child of the caverns. Few emerge from the depths unchanged… but you seem untouched by shadow — for now.'",
    "Eternal Innkeeper: 'The Eternal Sanctuary welcomes you. May the night be kind, and your burdens fade with the dawn.'"
]
def eternal_inkeeper_greeting():
    print(random.choice(eternal_inkeeper_lines_greet))

# Eternal Inkeeper says bye to player
eternal_inkeeper_lines_bye = [
    "Eternal Innkeeper: 'May your path stay lit, traveler. The Sanctuary’s doors will always open for you.'",
    "Eternal Innkeeper: 'Rest easy on your journey — and remember, light fades, but not forever.'",
    "Eternal Innkeeper: 'Travel safe, wanderer. The world beyond these walls is less kind than it seems.'",
    "Eternal Innkeeper: 'Until next we meet, may the Eternal flame guide your steps.'",
    "Eternal Innkeeper: 'The shadows wait outside, but fear not — the Sanctuary remembers you.'",
    "Eternal Innkeeper: 'Go with peace in your heart, and may the dawn greet you kindly, traveler.'"
]
def eternal_inkeeper_farewell():
    print(random.choice(eternal_inkeeper_lines_bye))

# Eternal Inkeeper says the history of Eternal Sanctuary
eternal_inkeeper_history_line = [
    "\nEternal Innkeeper: 'Aye… once, this place was naught but a humble village beneath the stone — warm fires, simple folk, laughter by candlelight… before the crystal was unbound.'",
    "\nEternal Innkeeper: 'We were as you are once — of flesh and blood. But when the Old One shattered the Riftstone, light poured forth… and it changed us.'",
    "\nEternal Innkeeper: 'They say he sought only to heal the land… yet the crystal’s breath swept through our souls, and we awoke… different. Eternal, some would call it.'",
    "\nEternal Innkeeper: 'The glow you see in our eyes is not life’s warmth, traveler — it is the echo of that day when the caverns wept light.'",
    "\nEternal Innkeeper: 'Many forgot their faces… their names. The Old Man vanished into the depths, and the Eternal Caverns were born from his folly.'",
    "\nEternal Innkeeper: 'Some still whisper he lingers below — the one who broke the crystal. A savior to some… a curse to the rest of us.'"
]

def eternal_sanctuary_history():
    print(random.choice(eternal_inkeeper_history_line))

# Eternal Inkeeper says how the Eternal Being came to be
eternal_inkeeper_beings_history_line = [
    "\nEternal Innkeeper: 'How we came to look thus? Hah… the crystal’s light seeped into our veins, slow as dawn but certain as death.'",
    "\nEternal Innkeeper: 'When the Riftstone shattered, it sang — and its song rewrote our flesh. Skin turned to shimmer, eyes to glow. We became the echoes of what we were.'",
    "\nEternal Innkeeper: 'We did not die that day, nor did we live on. The light bound our souls to this cavern… eternal, aye, but hollowed inside.'",
    "\nEternal Innkeeper: 'The glow you see, traveler, is not a blessing. It is the remnant of that crystal’s curse — forever reminding us of what we lost.'",
    "\nEternal Innkeeper: 'Our children ceased to age, our hearts ceased to beat. Yet still, we walk… and the caverns hum softly with our borrowed life.'",
    "\nEternal Innkeeper: 'The Old One called it salvation — but I’ve lived long enough to know mercy and madness oft wear the same face.'"
]
def eternal_beings_history():
    print(random.choice(eternal_inkeeper_beings_history_line))

# Eternal Inkeeper says how they get their stocks of food and items
eternal_village_survival_info = [
    "\nEternal Innkeeper: 'Ah, a fair question, traveler. The surface folk think us starved, yet the caverns provide more than ye’d reckon.'",
    "\nEternal Innkeeper: 'Glowcap mushrooms feed us, their roots drinking from the crystal’s light. Some say they taste of moonlight itself.'",
    "\nEternal Innkeeper: 'Our hunters tread the deeper tunnels, where beasts of the old world still roam. Their hides warm us, their meat sustains us.'",
    "\nEternal Innkeeper: 'The crystal veins hum with strange energies — we trade their shards with wanderers bold enough to brave the descent.'",
    "\nEternal Innkeeper: 'As for ale and spice, well, the spirits brew their own magic here. Even a cup of mead hums faintly with the Rift’s whisper.'",
    "\nEternal Innkeeper: 'We’ve long since learned to live beneath the stone. The Eternal Village endures — half by craft, half by miracle.'"
]
def eternal_villagers_survival():
    print(random.choice(eternal_village_survival_info))

# Eternal Inkeeper says some gossips
eternal_village_gossips = [
    "\nEternal Innkeeper: 'They say the Old Man once walked these halls as a scholar… before he sought to master the crystal’s heart.'",
    "\nEternal Innkeeper: 'Aye, Lance the Grandmaster? A noble soul, that one. But even his blade could not cut through what the Old Man became.'",
    "\nEternal Innkeeper: 'Some nights, I hear whispers from the lower caverns — voices begging for light that never comes.'",
    "\nEternal Innkeeper: 'A traveler once claimed he saw the Old Man’s reflection in the crystal veins… though the veins run deep below.'",
    "\nEternal Innkeeper: 'Before the crystal cracked, the Eternal Village had sky and wind… now we have only glow and shadow.'",
    "\nEternal Innkeeper: 'The Grandmaster was once his closest ally, or so the tales say. Two minds chasing truth — one found madness.'",
    "\nEternal Innkeeper: 'Our children are born with eyes of light now. Some call it a blessing… others a curse of the crystal’s breath.'",
    "\nEternal Innkeeper: 'The beasts outside the sanctum used to be men, they say. Twisted by the same light that grants us life.'",
    "\nEternal Innkeeper: 'A strange calm lingers before each quake in the caverns — as if the crystal itself draws breath.'",
    "\nEternal Innkeeper: 'They say Lance forged his blade not in fire, but in regret — tempered by what he failed to protect.'",
    "\nEternal Innkeeper: 'When the Old Man shattered the rift, he promised salvation. He gave us eternity… but stripped away our dawns.'",
    "\nEternal Innkeeper: 'Some of the villagers still pray to the Old Man’s name, believing he watches from beyond the crystal glare.'",
    "\nEternal Innkeeper: 'The Grandmaster no longer speaks his old friend’s name. Perhaps silence is the only penance left.'",
    "\nEternal Innkeeper: 'The further you walk from the Eternal Sanctuary, the louder the crystal hums. It does not like the living to stray.'",
    "\nEternal Innkeeper: 'Mind your dreams, traveler. The Old Man visits those who listen too long to the hum in the stone.'"
]
def eternal_inkeeper_gossip():
    print(random.choice(eternal_village_gossips))

# Soulwarden greeting the player when the player rents in the Eternal SAnctuary
soulwarden_greets = [

    "\nThe Soulwarden: 'Rest now, weary soul. The Sanctuary shall cradle thy spirit in silence.'",
    "\nThe Soulwarden: 'The Eternal Sanctuary welcomes thee once more. May thy dreams be light, and thy burdens fade.'",
    "\nThe Soulwarden: 'Peace finds all who walk beneath these sacred arches. Sleep, and awaken renewed.'",
    "\nThe Soulwarden: 'The caverns beyond are cruel and cold, but within these walls, thou art safe.'",
    "\nThe Soulwarden: 'Lay down thy arms, traveler. Here, no blade nor shadow may reach thee.'",
    "\nThe Soulwarden: 'Close thine eyes. The Sanctuary shall guard thy soul till dawn’s first breath.'"
]
def soulwarden_greetings_lines():
    print(random.choice(soulwarden_greets))
# Soulwarden says bye to player
def soulwarden_farwell(player_name):
    soulwarden_farewell_lines = [
        "Soulwarden: 'Go with peace, wanderer. The caverns remember those who tread them with courage.'",
        "Soulwarden: 'The light of the Sanctuary shall follow you, even in the deepest dark.'",
        f"Soulwarden: 'Return when your soul grows weary once more, {player_name}… this place awaits thee always.'",
        "Soulwarden: 'The paths beyond are perilous — but so too is stagnation. Move forward, as all must.'",
        "Soulwarden: 'May your spirit not falter, nor your blade grow dull.'",
        "Soulwarden: 'Do not forget… even stone remembers the warmth of light.'",
        "Soulwarden: 'Rest has mended your body. Now, go mend the world that still bleeds beyond these halls.'",
        f"Soulwarden: 'I have seen many come, few return. Prove thy tale shall not end in the shadows, {player_name}.'",
        "Soulwarden: 'The Eternal Sanctuary closes its embrace… until fate draws you back once more.'",
        "Soulwarden: 'May your courage outshine the darkness beneath the caverns, traveler.'"
    ]
    print(random.choice(soulwarden_farewell_lines))

# Eternal sacntuary restaurant SERAH
serah_lines = [
    "Serah of Sustenance: Ah, traveler… hunger still finds you. Come, see what I’ve prepared.",
    "Serah of Sustenance: Welcome. The hearth’s warmth waits for you.",
    "Serah of Sustenance: Sit, dear one. A good meal heals more than wounds.",
    "Serah of Sustenance: You look starved! Let’s see what comforts I can offer.",
    "Serah of Sustenance: Even heroes need supper. Come, take a look.",
    "Serah of Sustenance: The Sanctuary hums tonight… perhaps it knows you’re hungry."
]
def serah_line():
    print(random.choice(serah_lines))