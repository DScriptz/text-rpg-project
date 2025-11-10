import random

kaelith_lines = [
    "\nKaelith the Emberwright: 'Aye, traveler — the forge remembers every flame. What’ll ye have forged today?'",
    "\nKaelith the Emberwright: 'Every strike of my hammer costs more than gold — it costs a piece of me soul.'",
    "\nKaelith the Emberwright: 'Pickaxes, eh? A tool to dig deep, but remember — the stone bites back if ye’re careless.'",
    "\nKaelith the Emberwright: 'Ye can tell a miner’s worth by the glow on their pick, not the gold in their purse.'",
    "\nKaelith the Emberwright: 'My father forged blades for kings… me? I forge hope for fools who dig too deep.'",
    "\nKaelith the Emberwright: 'Don’t touch the embersteel till it cools — unless ye fancy glowin’ red as the forge itself.'"
]

def show_kaelith_lines():
    print(random.choice(kaelith_lines))

lady_gele_lines = [
    "\nLady Gele: 'Welcome, child of the surface. The spores hum softly today — a good omen for trade.'",
    "\nLady Gele: 'Each root remembers where it grew, each spore where it fell. Do you, traveler, remember your worth?'",
    "\nLady Gele: 'Mycelium weaves through everything — soil, stone, even sorrow. What would you trade to feel its song?'",
    "\nLady Gele: 'Gold is hollow, but spores… spores live. They grow in pockets of hope and decay alike.'",
    "\nLady Gele: 'Take care with what you purchase, dear one. Some things here bloom best in darkness.'",
    "\nLady Gele: 'Listen closely — can you hear it? The market breathes through the mycelium beneath your feet.'"
]

def show_lady_gele_lines():
    print(random.choice(lady_gele_lines))