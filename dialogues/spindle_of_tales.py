import random

# Loreweaver greets player
loreweaver_greets = [
    "\nLoreweaver: Ah… a traveler steps through my door. The Caverns whisper your tale already.",
    "\nLoreweaver: Welcome, seeker. These shelves hold the stories of both the living… and the forgotten.",
    "\nLoreweaver: Sit, child of the surface. The Eternal Village has waited long for a listener.",
    "\nLoreweaver: The threads of fate tremble around you, as though your arrival was written in ancient ink.",
    "\nLoreweaver: Shh… listen. Can you hear it? The Caverns themselves hum with your destiny."
]
def loreweaver_greet_lines():
    print(random.choice(loreweaver_greets))
# Loreweaver tasks the player to find an item for Enchanted Scroll decoding
loreweaver_quest = [

    "\nLoreweaver: This scroll resists my sight. Bring me the Emberleaf Blossom, and its story will unfold.",
    "\nLoreweaver: Only a rare touch can awaken these runes. Find the Emberleaf Blossom, and we shall see its secrets.",
    "\nLoreweaver: The magic here is stubborn. Seek the Emberleaf Blossom for me; the scroll cannot speak without it.",
    "\nLoreweaver: I can sense the tale within, but it slumbers. Retrieve the Emberleaf Blossom, and I will rouse it.",
    "\nLoreweaver: A simple leaf, yet its essence is the key. Bring me the Emberleaf Blossom, and the scroll shall reveal all.",
    "\nLoreweaver: You have done well to find this scroll, but it waits for a catalyst. Seek the Emberleaf Blossom, and its voice will awaken."
]
def loreweaver_quest_lines():
    print(random.choice(loreweaver_quest))
# Loreweaver Farewell to the player
loreweaver_farewell = [

    "\nLoreweaver: Go with care, traveler. The threads of fate are never idle.",
    "\nLoreweaver: May the stories guide your steps… until we meet again.",
    "\nLoreweaver: Walk carefully, for the world is full of tales both light and dark.",
    "\nLoreweaver: Return safely, and bring with you the whispers of your journey.",
    "\nLoreweaver: The scrolls will wait, but time does not. Farewell for now.",
    "\nLoreweaver: Step lightly, seeker. Your story is only beginning."
]
def loreweaver_farewell_lines():
    print(random.choice(loreweaver_farewell))
# THREAD OF FATE RANDOM LINES FOR PLAYER
def thread_of_fate(player_name):
    thread_of_fate_lines =[
        f"\n“A shadow travels beside you {player_name}, but only in darkness will it reveal its true face.”",
        "\n“Your hands will heal what your blade cannot strike — yet the cost will weigh heavy.”",
        "\n“A blossom of ember burns in the deep; its glow will either save or doom you.”",
        "\n“The old one’s path winds like a serpent; beware the bite at the journey’s end.”",
        "\n“A forgotten ally waits beneath stone and echo, loyal only to the brave.”",
        "\n“Fate twists your name into two endings — only one hand will guide it.”",
        "\n“The cavern will echo your scream or your triumph; the choice is not yet made.”",
        "\n“You will drink from a silver cup and learn it carries both poison and power.”",
        "\n“An ancient door sealed by sorrow will open at your touch — and you will not walk away unchanged.”",
        "\n“In the darkest passage, you’ll find a light that is not your own — follow or be swallowed.”"
    ]
    print(random.choice(thread_of_fate_lines))