from colorama import Fore, init, Style

init(autoreset=True)

""" GLIMMERPICK FORGE PICKAXES FOR SALE """
glimmerpick_pickaxes = {
    "Glowforged Pickaxe": {
        "name": "Glowforged Pickaxe",
        "price": 25,
        "damage": 5,
        "durability": 25
    },
    "Ironvein Pickaxe": {
        "name": "Ironvein Pickaxe",
        "price": 35,
        "damage": 8,
        "durability": 35
    },
    "Runic Digger": {
        "name": "Runic Dagger",
        "price": 50,
        "damage": 13,
        "durability": 45
    },
    "Extractinator Drill": {
        "name": "Extractinator Drill",
        "price": 60,
        "damage": 17,
        "durability": 55
    },
    "Crystal Carver": {
        "name": "Crystal Carver",
        "price": 75,
        "damage": 20,
        "durability": 70
    },
}

""" MYCELIUM EXCHANGE ITEMS FOR EXCHANGE """

mycelium_exchange_stocks = {
    "Gem": {
        "name": "Gem",
        "currency": {"type": "gold", "amount": 25},
        "desc": "A rare hidden gem that can only be found when mining some ores..."
    },
    "Stone": {
        "name": "Stone",
        "currency": {"type": "gold", "amount": 16},
        "desc": "A chunk of dense cavern rock, worn smooth by time. Common but useful — the bones of the underworld itself."
    },
    "Sporestone Fragment": {
        "name": "Sporestone Fragment",
        "currency": {"type": "item", "name": "Spore Cluster", "amount": 3},
        "desc": "A shard of mineral fused with living fungus. It hums faintly, as if remembering the rhythm of growth."
    },
    "Esscence of Decay": {
        'name': "Esscence of Decay",
        "currency": {"type": "item", "name": "Frozen Essence", "amount": 5},
        "desc": "A vial of slow death — distilled from rotting spores. Dangerous, but prized by those who shape life from ruin."
    },

}

