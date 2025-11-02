import random


# Shopkeeper Beth when player don't have enough gold lol broke
shop1_no_gold = [

    '\n"Shopkeeper: Ho there, traveler! Thy purse be empty. Come back when it holdeth coin."',
    '\n"Shopkeeper: Thou canst not buy that with naught but lint and air."',
    '\n"Shopkeeper: Hah! Do ye fancy taking wares without paying? Not on my watch!"',
    '\n"Shopkeeper: Thy pockets be as light as a feather. I’ll sell thee nothing this day."',
    '\n"Shopkeeper: Nay, friend. The coin is wanting, and my goods are not free for the asking."',
    '\n"Shopkeeper: Fie! Thou wouldst rob me with thine empty purse? Best return with coin."',
    '\n"Shopkeeper: The shelves are full, yet thy gold is naught. Come again when thy purse is heavier."',
    '\n"Shopkeeper: By my wares, thy coin falls short. Spend wisely, traveler."',
    '\n"Shopkeeper: Thou hast not the means. These goods require more than thy pockets yield."',
    '\n"Shopkeeper: Gold lacking, good traveler. Only those with sufficient coin may partake."'
]
def shop1_broke():
    print(random.choice(shop1_no_gold))

# Shopkeeper Beth lines when the player buys potion
shop_1_potion = [
    "\nShopkeeper: Wise choice — better to heal than to keel, as my gran used to say.",
    "\nShopkeeper: Keep it corked ‘til the fighting’s done, or you’ll waste the magic.",
    "\nShopkeeper: A sip of that and you’ll feel life rush back faster than spring thaw.",
    "\nShopkeeper: Don’t drink it all at once unless you like burping light!",
    "\nShopkeeper: Always glad to sell health, traveller — far cheaper than a funeral."
]
def potion_buy():
    print(random.choice(shop_1_potion))

# Shopkeeper Beth lines when the player buys Silver amulet
shop_1_amulet = [
    "\nShopkeeper: Oh ho! A bit of shine for your strike — may it bite true.",
    "\nShopkeeper: That amulet’s older than the king’s crown but twice as reliable.",
    "\nShopkeeper: Wear it close to the heart; power travels better that way.",
    "\nShopkeeper: Silver’s not just pretty — it remembers every battle fought.",
    "\nShopkeeper: Don’t pawn it to a drunk bard; they’ll never grasp its worth."
]
def amulet_buy():
    print(random.choice(shop_1_amulet))

# Shopkeeper Beth lines when the player buys Iron Shield
shop_1_shield = [
    "\nShopkeeper: Solid choice — that shield’s saved more hides than I can count.",
    "\nShopkeeper: Hold it steady and it’ll hold you steady right back.",
    "\nShopkeeper: Iron from the northern forges, quenched in river ice — sturdy as they come.",
    "\nShopkeeper: A little polish now and then and it’ll outlast you.",
    "\nShopkeeper: Take it, swing it, bash with it — but don’t forget it’s your wall between life and the grave."
]
def shield_buy():
    print(random.choice(shop_1_shield))