# Welcome to my fun first project. Basically it's a combination of my favorite action RPGs (First started Sept 5, 2025)
# First personal project on Python: September update ARPG Alpha. For those who are testing this, this is still in the works so it's not polished yet. Ight thx
# I used AI, online resources and w3schools only for helping me understand each functions and variables and where to put the parameters only. Sep 11, 2025.
# Gameplay is based but not the same to: Dungeons and Dragons, Pokemon, and World of Warcraft (so far)...
# Thank you for playtesting! Hope yall enjoy
# IF YOU'RE PLAYING FOR THE FIRST TIME, I SUGGEST NOT TO SKIP THE DIALOGUE FOR MORE IMMERSION AND STORY CONTEXT
# Version: 10.29.3 Alpha (Questing and Arena update) updated Oct 29, 2025.
import random
import sys
import time
import json
import os
import pygame
from colorama import Fore, Style, init
init(autoreset=True)
# Game short sounds helper code
def play_sound(sound_name, volume=0.6 ):
    try:
        sound_path = os.path.join("sounds", f"{sound_name}.ogg")
        sound = pygame.mixer.Sound(sound_path)
        sound.set_volume(volume)
        sound.play()
    except Exception as e:
        print(f"[Sound Error] Couldn't play '{sound_name}': {e}")
# Game long sounds/musics helper code (loop version)
def play_music(music_name, volume=0.5, loop=True ):
    try:
        music_path = os.path.join("sounds", f"{music_name}.ogg")
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1 if loop else 0)
    except Exception as e:
        print(f"[Music Error] Couldn't play '{music_name}': {e}")
# Load enemy data
try:
    with open('enemy_data.json', 'r') as file:
        enemies = json.load(file)
except FileNotFoundError:
    print("Error: enemy_data.json is not found! Make sure the file is in the same folder as this script.")
    sys.exit()
# ============================================
#     GAME FLAGS/STATS AND STARTING DATAA
# ============================================
# Keywords for dicts
potion_keywords = [
    "potion",
    "draught",
    "elixir",
    "tonic",
    "tea",
    "vial"
]
# Player stats
gold = 30 # 30 fair start hmm
current_chapter = 0
player_inventory = {
    "empty vial": 0,
    "empty bottle": 0,

}
player_quests = {

}
def show_quest_log(quests):
    play_sound("open quest log", volume=0.7)
    print("=" * 25)
    print("       -QUEST LOG-")
    print("=" * 25)
    if not quests:
        print("You have no active quests.")
        time.sleep(1.5)
        return
    for quest_name, quest_data in quests.items():
        status = quest_data.get("status", "Unknown")
        description = quest_data.get("description", "")
        print(f"- {quest_name} [{status}]")
        if description:
            print(f"   > {description}")
        print()
    input("Press enter to continue:  ")
    play_sound("close quest log", volume=0.8)
def add_quest(quests, name, description):
    if name not in quests:
        quests[name] = {"status": "Ongoing", "description": description}
        play_sound("new quest", volume=0.7)
        print(f"\nNew Quest Added: {name}")
        print(f"   > {description}")
    else:
        print(f"\nYou already have the quest: {name}\n")
def complete_quest(quests, name):
    if name in quests:
        quests[name]["status"] = "Completed"
        print(f"\nQuest Completed: {Fore.MAGENTA + Style.BRIGHT}{name}{Style.RESET_ALL}!\n")
        play_sound("quest completed", volume=0.6)
    else:
        print(f"\nQuest '{name}' not found.\n")
# Potion data of player
potion_data = {
    "healing potion": {
        "heal": 10,
        "effect": None,
        "duration": 0,
    },
    "greater potion": {
        "heal": 20,
        "effect": None,
        "duration": 0
    },
    "eternal petal elixir": {
        "heal": 35,
        "effect": "regen_up",
        "value": 10,
        "duration": 2
    },
    "starleaf draught": {
        "heal": 30,
        "effect": "attack_up",
        "value": 0.15,
        "duration": 3
    },
    "whisperoot tonic": {
        "heal": 25,
        "effect": "damage_reduce",
        "value": 0.5,
        "duration": 2
    },
    "dreamdew vial": {
        "heal": 35,
        "effect": "cure",
        "value": None,
        "duration": 0
    },
    "moonfern tea": {
        "heal": 45,
        "effect": "dodge_up",
        "value": 0.1,
        "duration": 2
    },
    "lunaris elixir": {
        "heal": 60,
        "effect": "invulnerable",
        "value": 1,
        "duration": 1
    }

}
# Potion list

potion_list = {

}
# Echo vials trading code
def echo_vials_trade(player_inventory, gold):
    print("========================================================================================================")
    print("                                         <-- Items To Trade-->                                          ")
    for i, (item, price) in enumerate(echo_vials_trade_items.items(), start=1):
        print(f"                          [{i}] <{item}> -- {price} Gold")
    print("========================================================================================================")
    print("                                        [X] Exit Menu")
    print("                                        [I] Open Inventory")
    while True:
        trading = input(">>  ").lower().strip()
        if trading == "x":
            print("You walk away from the trading table...")
            break
        if not trading.isdigit() or int(trading) < 1 or int(trading) > len(echo_vials_trade_items):
            print()
            continue
        index = int(trading)
        item_name = list(echo_vials_trade_items.keys())[index - 1]
        item_price = echo_vials_trade_items[item_name]
        # Check amount the player wants to trade
        amount = int(input(f"How many {item_name}'s do you want to trade?: "))
        if item_name in player_inventory and player_inventory[item_name] >= amount:
            player_inventory[item_name] -= amount
            gold_earned = amount * item_price
            gold += gold_earned
            print(f"You sold {amount}x {item_name} for {gold_earned} Gold!")
        else:
            print(f"You don't have any {item_name} to trade!")
    return player_inventory, gold
# Potion list/ inventory of player
def potion_lists():
    print("----------- Potion List -------------")
    for key, value in potion_list.items():
        print(f"-> {key.title()}: {value}")
    print("------------------------------------")
# Player opens inventory in battle
def open_inventory():
    play_sound("inventory open", volume=0.8)
    print("\n--- INVENTORY ---")
    for item, amount in player_inventory.items():
        print(f"-> {item.title()}: {amount}")
    print("-------------------")
    print("Press Enter to close inventory")
    input("> ")
    play_sound("inventory close", volume=0.8)
# echoing vials stocks code
def echoing_vials_stocks():
    potion_stock = {}
    for potion in potion_data:
        roll = random.randint(1, 9)
        threshold = 6
        if roll <= threshold:
            potion_stock[potion] = random.randint(1, 3)
            print(f"{Fore.LIGHTGREEN_EX}-> {potion.title()} has {potion_stock[potion]} stock{Style.RESET_ALL}")
        else:
            potion_stock[potion] = 0
            print(f"{Fore.LIGHTBLACK_EX + Style.DIM}->> {potion.title()} is out of stock{Style.RESET_ALL}")
    return potion_stock
# Displaying the stocks for Echo vials
def echoing_vials_display_stock(potion_stock):
    for potion, amount in potion_stock.items():
        potion_names = potion.title()
        if amount <= 0:
            print(f"{Fore.LIGHTBLACK_EX + Style.DIM}->> {potion_names} is out of stock{Style.RESET_ALL}")
        else:
            print(f"{Fore.LIGHTGREEN_EX}-> {potion_names} has {amount} stock{Style.RESET_ALL}")
# shop choice code function
def shop_choice():
    global gold
    shop_stock = echoing_vials_stocks()
    while True:
        print("\n                               =========================================================================================================================================")
        print("                                                                                        --|-ECHOING VIALS MENU-|--                                                             ")
        print(f"\n                     --[{player_name}, {race_name} {player_class} | {Fore.RED}{player_health}{Style.RESET_ALL}/{Fore.RED}{max_health}{Style.RESET_ALL} HP | {gold} {Fore.LIGHTYELLOW_EX}Gold{Style.RESET_ALL}]--")
        print(
        "\n                                       [1]. Whisperoot Tonic (48 Gold, reduces damage taken by 50% for 2 turns) - A pale-green draught that hardens the body against harm."
        "\n                                       [2]. Eternal Petal Elixir (50 Gold, regenerates +10 HP for 2 turns) - A radiant violet vial that pulses with healing energy."
        "\n                                       [3]. Starleaf Draught (55 Gold, +15% Attack Power for 3 turns) - A glittering blue potion that hums with celestial might."
        "\n                                       [4]. Moonfern Tea (45 Gold, +10% dodge chance for 2 turns) - A faintly glowing brew that sharpens reflexes under moonlight."
        "\n                                       [5]. Dreamdew Vial (60 Gold, cures all negative effects) - A soothing red elixir said to calm both body and spirit."
        "\n                                       [6]. Lunaris Elixir (95 Gold, grants invulnerability for 1 turn, restores 60 HP) - A silver-white essence that shields the drinker in lunar light."
        "\n                                       [7]. Healing Potion (20 Gold) - A bright red draught that soothes minor wounds and restores a spark of vitality."
        "\n                                       [8]. Greater Healing Potion (25 gold) - A deep crimson elixir that radiates warmth, swiftly mending your wounds and invigorating your spirit."
        "\n                                       [X]. Exit Menu.")
        print("                              ============================================================================================================================================")
        time.sleep(0.3)
        menu_choice = input("                         Choice: >> ")
        if menu_choice == "1" and gold >= 48:
            potion_name = "whisperoot tonic"
            price = 48
            if shop_stock.get(potion_name, 0) <= 0:
                print(f"Sorry, {potion_name} is out of stock")
            else:
                if gold >= price:
                    gold -= price
                    shop_stock[potion_name] -= 1
                    potion_list[potion_name] = potion_list.get(potion_name, 0) + 1
                    player_payment()
                    print(f"You bought a {potion_name}! (-{price} gold). Gold left: {gold}")
        elif menu_choice == "2" and gold >= 50:
            potion_name = "eternal petal elixir"
            price = 60
            if shop_stock.get(potion_name, 0) <= 0:
                print(f"\n--Sorry, {potion_name} is out of stock!--")
            else:
                if gold >= price:
                    gold -= price
                    shop_stock[potion_name] -= 1
                    potion_list[potion_name] = potion_list.get(potion_name, 0) + 1
                    player_payment()
                    print(f"You bought a {potion_name}! (-{price} gold). Gold left: {gold}")
        elif menu_choice == "3" and gold >= 55:
            potion_name = "starleaf draught"
            price = 55
            if shop_stock.get(potion_name, 0) <=0:
                print(f"\nSorry, {potion_name} is out of stock!")
            else:
                if gold >= price:
                    gold -= price
                    shop_stock[potion_name] -= 1
                    potion_list[potion_name] = potion_list.get(potion_name, 0) + 1
                    player_payment()
                    print(f"You bought a {potion_name}! (-{price} gold). Gold left: {gold}")
        elif menu_choice == "4" and gold >= 45:
            potion_name = "moonfern tea"
            price = 45
            if shop_stock.get(potion_name, 0) <= 0:
                print(f"\nSorry, {potion_name} is out of stock!")
            else:
                if gold >= price:
                    gold -= price
                    shop_stock[potion_name] -= 1
                    potion_list[potion_name] = potion_list.get(potion_name, 0) + 1
                    player_payment()
                    print(f"You bought a {potion_name}! (-{price} gold). Gold left: {gold}")
        elif menu_choice == "5" and gold >= 60:
            potion_name = "dreamdew vial"
            price = 60
            if shop_stock.get(potion_name, 0) <= 0:
                print(f"\nSorry, {potion_name} is out of stock!")
            else:
                if gold >= price:
                    gold -= price
                    shop_stock[potion_name] -= 1
                    potion_list[potion_name] = potion_list.get(potion_name, 0) + 1
                    player_payment()
                    print(f"You bought a {potion_name}! (-{price} gold). Gold left: {gold}")
        elif menu_choice == "6" and gold >= 95:
            potion_name = "lunaris elixir"
            price = 95
            if shop_stock.get(potion_name, 0) <= 0:
                print(f"\nSorry, {potion_name} is out of stock!")
            else:
                if gold >= price:
                    gold -= price
                    shop_stock[potion_name] -= 1
                    potion_list[potion_name] = potion_list.get(potion_name, 0) + 1
                    player_payment()
                    print(f"You bought a {potion_name}! (-{price} gold). Gold left: {gold}")
        elif menu_choice == "7" and gold >= 20:
            potion_name = "healing potion"
            price = 20
            if shop_stock.get(potion_name, 0) <= 0:
                print(f"Sorry, {potion_name} is out of stock!")
            else:
                if gold >= price:
                    gold -= price
                    shop_stock[potion_name] -= 1
                    potion_list[potion_name] = potion_list.get(potion_name, 0) + 1
                    player_payment()
                    print(f"You bought a {potion_name}! (-{price} gold). Gold left: {gold}")
        elif menu_choice == "8" and gold >= 25:
            potion_name = "greater potion"
            price = 25
            if shop_stock.get(potion_name, 0) <= 0:
                print(f"Sorry, {potion_name} is out of stock!")
            else:
                if gold >= price:
                    gold -= price
                    shop_stock[potion_name] -= 1
                    potion_list[potion_name] = potion_list.get(potion_name, 0) + 1
                    player_payment()
                    print(f"You bought a {potion_name}! (-{price} gold). Gold left: {gold}")
        elif menu_choice == "x":
            echo_binder_farewell_line()
            time.sleep(1.6)
            break
        else:
            print("Invalid choice or Gold!")
        potion_lists()
        time.sleep(1.3)
        print("Current shop stock:")
        echoing_vials_display_stock(shop_stock)
        time.sleep(1.5)
# Player effect after donating
donate_effects = [

    "\nYour body feels lighter... (+10% dodge next battle)",
    "\nA warmth fills your chest... (+5 attack next battle)",
    "\nYour skin hardens faintly... (-10% damage taken next battle)",
    "\nA whisper echoes: 'Be swift...' (+1 speed next battle)",
    "\nYou feel calm and focused... (+5 HP regen next battle)"

]
def donated_effects():
    print(random.choice(donate_effects))
# Unique Abilities conditions
summoned = False  # for Necromancer
skill_cooldown = 4 # Special ability cooldowns
skill_cooldown_timer = 0
damage_multiplier = 1
dodging = False # for Rogue shadow step
holy_shield_active = False # for Paladin
enemy_confused = False # for Illusionist
enemy_confused_turns = 0
war_cry_turns = 0 # for Sentinel
# ------------------------------------ #
# temporary potions effect
regen_turns = 2
regen_effect = 10
attack_up_turns = 3
attack_up_effect = 0.15
defense_boost_turns = 2
defense_boost_effect = 0.5
dodge_up_turns = 2
dodge_up_effect = 0.1
invulnerable_turns = 1
invulnerable_effect = 1
damage_reduce_turns = 0
# Enemy debuff flags
reduced_enemy_defense = 0 # Debuff for enemy defense
reduced_enemy_attack = 0
# Bulwark Flags
bulwark_active = False # for Sentinel's Bulwark Stance
bulwark_turns = 2
bulwark_cd = 5
# Tavern (The Hollow Earth Inn) Drinks stocks
hearthfire_stock = 2
mead_stock = 2
spirits_stock = 1
# Tavern Variables
tavern_choice = ""
hp_change = random.randint(5, 15)
# Shop 2 Armor stocks
steel_cuirass_stock = 2
hauberk_stock = 3
knight_helm_stock = 5
gauntlets_grip_stock = 4
hide_cloak_stock = 3
boots_stoneguard_stock = 6
pauldrons_valor_stock = 3
bracers_fortitude_stock = 5
gorget_brave_stock = 5
shield_of_eternal_stock = 2
# Shop 2 Weapon stocks
ironfang_stock = 3
runed_sword_stock = 2
hammer_deep_forge_stock = 1
bow_whispering_pines_stock = 2
dagger_shadowglass_stock = 3
crossbow_silent_thunder_stock = 2
staff_emberlight_stock = 2
axe_stonebreaker_stock = 2
lance_eternal_guard_stock = 2
warblade_brave_stock = 1
eternal_roast_stock = 1
# Trader 1 stocks
# Goblin grunts
pygame.mixer.init()
grunt_1 = pygame.mixer.Sound(r"sounds/monster1.ogg")
grunt_2 = pygame.mixer.Sound(r"sounds/monster2.ogg")
def goblin_grunts():
    random.choice([grunt_1, grunt_2]).play()
# Land of Bravery Music
land_of_bravery = [
    r"sounds/land of bravery.ogg",
    r"sounds/land of bravery alt.ogg"
]
land_of_bravery_bgm = random.choice(land_of_bravery)
# eternal being Grunt
eternal_being_grunt1 = pygame.mixer.Sound(r"sounds/eternal being hurt.ogg")
eternal_being_grunt2 = pygame.mixer.Sound(r"sounds/eternal being hurt 2.ogg")

eternal_being_grunts = [eternal_being_grunt1, eternal_being_grunt2]
def eternal_being_grunt():
    random.choice([eternal_being_grunts]).play()
#  Player pays in shop 1
coin_sound = pygame.mixer.Sound(r"sounds/coin.ogg")
coin_sound2 = pygame.mixer.Sound(r"sounds/coin2.ogg")
coin_sound3 = pygame.mixer.Sound(r"sounds/coin3.ogg")

payment = [coin_sound, coin_sound2, coin_sound3]
def player_payment():
    random.choice(payment).play()
# Door opens
door_open_sound = pygame.mixer.Sound(r"sounds/open door.ogg")
door_open_sound2 = pygame.mixer.Sound(r"sounds/open door 2.ogg")

door_open = [door_open_sound, door_open_sound2]
def door_opening_sound():
    random.choice(door_open).play()
# Eternal Bartender lines
try:
    with open('eternal_bartender_lines.json', 'r') as file:
        eternal_bartender_lines = json.load(file)
except FileNotFoundError:
    print("Error: eternal_bartender_lines.json is not found!")
    eternal_bartender_lines("Greetings Human")
def speak_eternal_bartender():
    print(random.choice(eternal_bartender_lines))
# Echoing Vials trading Feature items
echo_vials_trade_items = {
    "Ashfang Carapace": 5,
    "Gleaming Fang": 6,
    "Thread of Valor": 8,
    "Spore Cluster": 8,
    "Myconid Cap": 10,
    "Luminescent Root": 12,
    "Shard of the Warden": 15,
    "Fractured Prism": 16,
    "Frostvein Dust": 18,
    "Veilstone Fragment": 16,
    "Harbringer's Ash": 17,
    "Crimson Dust": 19,
    "Echoing Ice Core": 20,
    "Soulfrost Fragment": 25,
    "Frozen Essence": 27,
    "Spectral Shard": 30,
    "Chillhound Cloth": 30,
    "Shattered Sigil": 35,
    "Hollowsteel Fragment": 37,
    "Eternal Guard Plate": 40,
    "Ebon Bone": 42,
    "Marrow Resin": 45,
    "Blackened Core": 47,
    "Ember Scale": 50,
    "Veilfire Heart": 52,
    "Cindered Fang": 55,
    "Vermillion Core": 60,
    "Tyrant's Horn": 65,
    "Ancient Blood Gem": 75
}
# Echo binder farewell lines-
echo_binder_farewell = [
    "\nEcho Binder: May your echoes guide you safely through the caverns.",
    "\nEcho Binder: Farewell, traveler. Let the whispers of the stones watch over you.",
    "\nEcho Binder: Until next time, may your path resonate with fortune.",
    "\nEcho Binder: Go well, and remember—the echoes never truly leave.",
    "\nEcho Binder: Safe travels, wanderer. Let the vials sing in your honor.",
    "\nEcho Binder: Part now, but carry the echoes of this place with you."
]
def echo_binder_farewell_line():
    print(random.choice(echo_binder_farewell))
# Eternal warrior and player convo
def player_eternal_warrior_talking():
    print("\nWhat will you say?")
    while True:
        choices = input("\n1. 'I have been sent by Lance, The Grandmaster, to investigate what's down here.'"
                       "\n2. 'The Poisonous Spider I killed dropped an Enchanted scroll, would you help me decode it?'"
                       "\n3. 'Bye.'\n> ").strip()

        # Player choices and eternal warrior talking
        if choices == "1":
            print("\nEternal Warrior: 'Oh, is that so? I think our king might have an answer for that..'")
            time.sleep(2)
            print("Eternal Warrior: 'I suggest taking this up to the King.'")
        elif choices == "2":
            print("\nEternal Warrior: 'Scroll? Hmm interesting... maybe the Loreweaver can help you with this matter.'")
            time.sleep(3)
        elif choices == "3":
            print("\nEternal Warrior: 'See you around, Traveller. You're welcome here.'")
            pygame.mixer.music.fadeout(2000)
            time.sleep(1)
            break
        else:
            print("\nEternal Warrior: 'You wanted to say something?'")
# Donating to the Eternal village on echo vials shop-------
def echo_vials_donation():
    global gold
    print()
    print("|---> Donation Table <---|")
    print("[1]. Donate Gold")
    print("[2]. Donate Empty Bottle of Potion")
    print("[3]. Check Inventory")
    print("[X]. Leave")
    print()
    donate = input("\n> ").strip()
    if donate == "1":
        print("How much gold will you want to donate?")
        donation_amount = int(input("\n> "))
        if 0 < donation_amount <= gold:
            gold -= donation_amount
            print(f"You donated {donation_amount} gold. The bowl glows softly")
            time.sleep(1.3)
            donated_effects()
    elif donate == "2":
        item_name = "Empty Bottle"
        remaining = player_inventory.get("empty bottle, 0")
        if player_inventory.get("empty bottle", 0) > 0:
            player_inventory["empty bottle"] -= 1
            print("You have placed an empty bottle. It hums quietly...")
            print(f"- 1{item_name} (Empty Bottle remaining: {remaining})")
            time.sleep(1.3)
            donated_effects()
        else:
            print("You have no vials or bottles to donate")
    elif donate == "3":
        print("You open your inventory...")
        time.sleep(1.2)
        open_inventory()
    else:
        print("You step away from the table.")

# Shop 2 Trader shop functionnnnnnn
def trader_shop():
    global gold, attack_max, max_health, player_health
    print()
    print("=================================================================================================================================================")
    print("                                                          -TRADER'S OFFERS-                                                                      ")
    print(f"    {Fore.LIGHTRED_EX}[1]. Greater Healing Potion{Style.RESET_ALL} (6 {Fore.LIGHTYELLOW_EX}gold{Style.RESET_ALL}) +20 HP healed")
    print(f"    {Fore.LIGHTMAGENTA_EX}[2]. Crystal of Demise{Style.RESET_ALL} (11 {Fore.LIGHTYELLOW_EX}gold{Style.RESET_ALL}, +6 attack)")
    print(f"    {Fore.LIGHTCYAN_EX}[3]. Magic Ring{Style.RESET_ALL} (12 {Fore.LIGHTYELLOW_EX}gold{Style.RESET_ALL}, +10 max HP)")
    print(f"    {Fore.MAGENTA + Style.DIM}[4]. Gambling Potion{Style.RESET_ALL} (20 {Fore.LIGHTYELLOW_EX}gold{Style.RESET_ALL}, may increase player's attack...)")
    print(f"    {Style.BRIGHT}[5]. Leave the Trader{Style.RESET_ALL}")
    print(f"    [Q]. {Style.BRIGHT}Show Quests.")

    print("=================================================================================================================================================")
    # Shop 2, Trader shop code
    while True:
        print(f"\n                                          --[{player_name}, {race_name} {player_class} | {Fore.RED}{player_health}{Style.RESET_ALL}/{Fore.RED}{max_health}{Style.RESET_ALL} HP | {gold} {Fore.LIGHTYELLOW_EX}Gold{Style.RESET_ALL}]--")
        trade = input("\nWhat do you want to buy? (1/2/3/4/5): ")
        if trade == "1" and gold >= 6:
            base_price = 6
            item_bought = "Greater Potion".lower()
            if race_name.lower() == "human":
                player_payment()
                print("Trader Silas: Yes my companion, thy are in my favor!")
                price = base_price - 1
                print(f"You have bought a Greater Healing Potion with a discounted price (-1 Gold)!")
            else:
                price = base_price
                player_payment()
                print("You have bought a Greater Healing Potion!")
            gold -= price
            potion_list[item_bought] = potion_list.get(item_bought, 0) + 1
            print(f"(Greater Healing Potions: {potion_list['greater potion']}, Gold: {gold})")
        elif trade == "2" and gold >= 11:
            player_payment()
            attack_max += 6
            gold -= 11
            print(f"You have bought a Crystal of Demise! (Attack max: {attack_max}, Gold: {gold})")
        elif trade == "3" and gold >= 12:
            player_payment()
            max_health += 10
            player_health += 5
            gold -= 12
            print(f"You have bought a Magic Ring! (Player Health: {player_health}/{max_health}, Gold: {gold})")
        elif trade == "4" and gold >= 20:
            player_payment()
            attack_max += random.randint(0, 15)
            gold -= 20
            print(f"You have bought a Gambling Potion and drank it! (Max attack is now {attack_max} Gold: {gold})")
        elif trade == "5":
            print("\nThe Lost Trader: Well then, be careful down there...")
            print("\nYou leave the trader and go deeper into the cave…")
            break
        elif trade == "q":
            show_quest_log(player_quests)
        else:
            print("\nLost Trader Silas: If you don't have enough coins, speak!")
# Shop 3, Stoneheart armory function
def stoneheart_armory_shop():
    global player_name, max_health, player_health, attack_max, gold
    global steel_cuirass_stock, mead_stock, ironfang_stock, spirits_stock, knight_helm_stock, gauntlets_grip_stock, hide_cloak_stock, boots_stoneguard_stock, bracers_fortitude_stock, gorget_brave_stock, shield_of_eternal_stock
    global hauberk_stock, runed_sword_stock, hammer_deep_forge_stock, bow_whispering_pines_stock, dagger_shadowglass_stock, axe_stonebreaker_stock, lance_eternal_guard_stock, staff_emberlight_stock, crossbow_silent_thunder_stock, warblade_brave_stock, pauldrons_valor_stock
    while True:
        shop2_move = input("What do you want to do?: "
                           "\n--> 1. Buy Armors (HP increasing items)."
                           "\n--> 2. Buy Weapons (Attack increasing items)."
                           "\n--> 3. Leave Stoneheart Armory.\n> ").strip()
        # Menu for the Armors
        shop2_armorer_visit()
        if shop2_move.strip() == "1":
            while True:
                print(f"\n                     --[{player_name}, {race_name} {player_class} | {Fore.RED}{player_health}{Style.RESET_ALL}/{Fore.RED}{max_health}{Style.RESET_ALL} HP | {gold} {Fore.LIGHTYELLOW_EX}Gold{Style.RESET_ALL}]--")
                print("What will you buy?")
                time.sleep(1)
                shop2_buy= input("\nArmors for sale:"
                      f"\n[1]. {Fore.LIGHTCYAN_EX}Steel Cuirass{Style.RESET_ALL} (65 {Fore.LIGHTYELLOW_EX}Gold{Style.RESET_ALL}, +40 Max HP, {steel_cuirass_stock} in stock) – 'Forged from the eternal iron veins, this breastplate hath saved many a soul.'"
                      f"\n[2]. {Fore.WHITE}Chainmail Hauberk{Style.RESET_ALL} (50 {Fore.LIGHTYELLOW_EX}Gold{Style.RESET_ALL}, +30 Max HP, {hauberk_stock} in stock) – 'Light of weight, yet stout against the sharpest of blades.'"
                      f"\n[3]. {Fore.YELLOW}Knight's Helm{Style.RESET_ALL} (25 {Fore.LIGHTYELLOW_EX}Gold{Style.RESET_ALL}, +15 HP, {knight_helm_stock} in stock) - 'Guard thy head as if by ancient enchantment'"
                      f"\n[4]. {Fore. LIGHTGREEN_EX}Gauntlets of Grip{Style.RESET_ALL} (25 {Fore.LIGHTYELLOW_EX}Gold{Style.RESET_ALL}, +5 Max attack, +10 Max HP, {gauntlets_grip_stock} in stock) - 'Firm upon thy hands, for both battle and craft'"
                      f"\n[5]. {Fore.LIGHTYELLOW_EX}Reinforced Hide Cloak{Style.RESET_ALL} (40 {Fore.LIGHTYELLOW_EX}Gold{Style.RESET_ALL}, +20 Max HP, {hide_cloak_stock} in stock) - 'Keeps thee hidden and unharmed in shadowed halls'"
                      f"\n[6]. {Fore.LIGHTBLACK_EX}Boots of Stoneguard{Style.RESET_ALL} (20 {Fore.LIGHTYELLOW_EX}Gold{Style.RESET_ALL}, +10 Max HP, {boots_stoneguard_stock} in stock) - 'Shield thy feet, lest the caverns' stone bite thee sorely'"
                      f"\n[7]. {Fore.MAGENTA}Pauldrons of Valor{Style.RESET_ALL} (35 {Fore.LIGHTYELLOW_EX}Gold{Style.RESET_ALL}, +15 Max HP, +7 Attack, {pauldrons_valor_stock} in stock) - 'Shoulder guards that turn aside the fiercest strike'"
                      f"\n[8]. {Fore.GREEN}Bracers of Fortitude{Style.RESET_ALL} (20 {Fore.LIGHTYELLOW_EX}Gold{Style.RESET_ALL}, +10 Max HP, +3 Max Attack, {bracers_fortitude_stock} in stock) - 'Defend thy forearms with strength and resolve'"
                      f"\n[9]. {Fore.BLUE}Gorget of the Brave{Style.RESET_ALL} (20 {Fore.LIGHTYELLOW_EX}Gold{Style.RESET_ALL}, +8 Max HP, +4 Max Attack, {gorget_brave_stock} in stock) - 'A neckguard for the daring, for those who face danger head on.'"
                      f"\n[10]. {Fore.CYAN}Shield of the Eternal Caverns{Style.RESET_ALL} (55 {Fore.LIGHTYELLOW_EX}Gold{Style.RESET_ALL}, +30 Max HP, +7 Max Attack, {shield_of_eternal_stock} in stock) - 'Endures the deepest fights, steadfast as stone.'"
                                 "\nX. Exit Menu."
                                  "\n--> ")
                if shop2_buy.strip().lower() == "x":
                    print(f"{player_name}: I, thank you, Armorer for thy service.")
                    time.sleep(1)
                    shop2_stoneheart_armorer_bye()
                    time.sleep(2)
                    break
                elif shop2_buy.strip() == "1" and gold >= 65:
                    if steel_cuirass_stock > 0:
                        player_payment()
                        steel_cuirass_stock -= 1
                        gold -= 65
                        max_health += 40
                        print(f"{player_name}: 'I'll take the {Fore.LIGHTCYAN_EX}Steel Cuirass{Style.RESET_ALL} - may its iron veins guard my soul as the caverns guard their secrets.'")
                        time.sleep(2)
                        shop2_cuirass_buy()
                        time.sleep(1)
                        print(f"You bought {Fore.LIGHTCYAN_EX}Steel Cuirass{Style.RESET_ALL}! +40 Max HP. Max health is now {max_health}.")
                elif shop2_buy.strip() == "2" and gold >= 50:
                    if hauberk_stock > 0:
                        player_payment()
                        hauberk_stock -= 1
                        gold -= 50
                        max_health += 30
                        print(f"{player_name}: '{Fore.WHITE}Chainmail Hauberk{Style.RESET_ALL} for me - light enough to move, stout enough to endure.'")
                        time.sleep(2)
                        shop2_hauberk_buy()
                        time.sleep(1)
                        print(f"You bought {Fore.WHITE}Chainmail Hauberk{Style.RESET_ALL}! +30 Max HP. Max health is now {max_health}.")
                    else:
                        print("Eternal Armorer: 'Oi! Either you don't have the gold or I don't have stocks!'")
                elif shop2_buy.strip() == "3" and gold >= 25:
                    if knight_helm_stock > 0:
                        player_payment()
                        knight_helm_stock -= 1
                        gold -= 25
                        max_health += 15
                        print(f"{player_name}: 'This {Fore.YELLOW}Knight's Helm{Style.RESET_ALL} shall keep my wits and skull unbroken in battle.'")
                        time.sleep(2)
                        shop2_helm_buy()
                        time.sleep(1)
                        print(f"You bought {Fore.YELLOW}Knight's Helm{Style.RESET_ALL}! +15 Max HP. Max health is now {max_health}.")
                    else:
                        print("Eternal Armorer: 'Oi! Either you don't have the gold or I don't have stocks!'")
                elif shop2_buy.strip() == "4" and gold >= 25:
                    if gauntlets_grip_stock > 0:
                        player_payment()
                        gauntlets_grip_stock -= 1
                        gold -= 25
                        attack_max += 5
                        print(f"{player_name}: 'I'll don the {Fore. LIGHTGREEN_EX}Gauntlets of Grip{Style.RESET_ALL} - my strike shall be sure and my grasp unyielding.'")
                        time.sleep(2)
                        max_health += 10
                        shop2_gauntlets_grip_buy()
                        time.sleep(1)
                        print(f"You bought {Fore. LIGHTGREEN_EX}Gauntlets of the Grip{Style.RESET_ALL}! +5 Max attack & +10 Max HP. Max health is now {max_health}"
                              f" and max Attack is now {attack_max}.")
                    else:
                        print("Eternal Armorer: 'Oi! Either you don't have the gold or I don't have stocks!'")
                elif shop2_buy.strip() == "5" and gold >= 40:
                    if hide_cloak_stock > 0:
                        player_payment()
                        hide_cloak_stock -= 1
                        gold -= 40
                        max_health += 20
                        print(f"{player_name}: 'This {Fore.LIGHTYELLOW_EX}Reinforced Hide Cloak{Style.RESET_ALL} shall shield me in the shadows and the fray alike.'")
                        time.sleep(2)
                        shop2_reinforced_hide_cloak_buy()
                        time.sleep(1)
                        print(f"You bought the {Fore.LIGHTYELLOW_EX}Reinforced Hide Cloak{Style.RESET_ALL}! +20 Max HP. Max health is now {max_health}.")
                    else:
                        print("Eternal Armorer: 'Oi! Either you don't have the gold or I don't have stocks!'")
                elif shop2_buy.strip() == "6" and gold >= 20:
                    if boots_stoneguard_stock > 0:
                        player_payment()
                        boots_stoneguard_stock -= 1
                        gold -= 20
                        max_health += 10
                        print(f"{player_name}: 'With these {Fore.LIGHTBLACK_EX}Boots of Stoneguard{Style.RESET_ALL}, I'll walk the cavern roads unwearied and unbroken.'")
                        time.sleep(2)
                        shop2_boots_of_stoneguard_buy()
                        time.sleep(1)
                        print(f"You bought {Fore.LIGHTBLACK_EX}Boots of Stoneguard{Style.RESET_ALL}! +10 Max HP. Max health is now {max_health}.")
                    else:
                        print("Eternal Armorer: 'Oi! Either you don't have the gold or I don't have stocks!'")
                elif shop2_buy.strip() == "7" and gold >= 35:
                    if pauldrons_valor_stock > 0:
                        player_payment()
                        pauldrons_valor_stock -= 1
                        gold -= 35
                        max_health += 15
                        attack_max += 7
                        print(f"{player_name}: '{Fore.MAGENTA}Pauldrons of Valor{Style.RESET_ALL} - I'll shoulder the weight of battle and strike with honor.'")
                        time.sleep(2)
                        shop2_pauldrons_of_valor_buy()
                        time.sleep(1)
                        print(f"You bought {Fore.MAGENTA}Pauldrons of Valor{Style.RESET_ALL}! +15 Max HP & +7 Max Attack. Max health is now {max_health} &"
                              f" Max Attack is now {attack_max}.")
                    else:
                        print("Eternal Armorer: 'Oi! Either you don't have the gold or I don't have stocks!'")
                elif shop2_buy.strip() == "8" and gold >= 20:
                    if bracers_fortitude_stock > 0:
                        player_payment()
                        bracers_fortitude_stock -= 1
                        gold -= 20
                        max_health += 10
                        attack_max += 3
                        print(f"{player_name}: '{Fore.GREEN}Bracers of Fortitude{Style.RESET_ALL}, to steady my arm and steel my resolve.'")
                        time.sleep(2)
                        shop2_bracers_of_fortitude_buy()
                        time.sleep(1)
                        print(f"You bought {Fore.GREEN}Bracers of Fortitude{Style.RESET_ALL}! +10 Max HP & +3 Max Attack. Max health is now {max_health} &"
                              f" Max Attack is now {attack_max}")
                    else:
                        print("Eternal Armorer: 'Oi! Either you don't have the gold or I don't have stocks!'")
                elif shop2_buy.strip() == "9" and gold >= 20:
                    if gorget_brave_stock > 0:
                        player_payment()
                        gorget_brave_stock -= 1
                        gold -= 20
                        max_health += 8
                        attack_max += 4
                        print(f"{player_name}: 'This {Fore.BLUE}Gorget of the Brave{Style.RESET_ALL} shall guard my throat and proclaim my courage.'")
                        time.sleep(2)
                        shop2_gorget_of_the_brave_buy()
                        time.sleep(1)
                        print(f"You bought {Fore.BLUE}Gorget of the Brave{Style.RESET_ALL}! +8 Max HP & +4 Max Attack. Max Health is now {max_health} &"
                              f" Max Attack is now {attack_max}.")
                    else:
                        print("Eternal Armorer: 'Oi! Either you don't have the gold or I don't have stocks!'")
                elif shop2_buy.strip() == "10" and gold >= 55:
                    if shield_of_eternal_stock > 0:
                        player_payment()
                        shield_of_eternal_stock -= 1
                        gold -= 55
                        max_health += 30
                        attack_max += 7
                        print(f"{player_name}: 'I'll wield the {Fore.CYAN}Shield of the Eternal Caverns{Style.RESET_ALL} - steadfast as the stone itself.'")
                        time.sleep(2)
                        shop2_shield_of_eternal_caverns_buy()
                        time.sleep(1)
                        print(f"You bought {Fore.CYAN}Shield of the Eternal Caverns{Style.RESET_ALL}! +30 Max HP & +7 Max Attack. Max health is now {max_health}.")
                    else:
                            print("Eternal Armorer: 'Oi! Either you don't have the gold or I don't have stocks!'")
                else:
                    print("Not enough gold or invalid option.")
        elif shop2_move.strip() == "2":
            while True:
                print(f"\n                     --[{player_name}, {race_name} {player_class} | {Fore.RED}{player_health}{Style.RESET_ALL}/{Fore.RED}{max_health}{Style.RESET_ALL} HP | {gold} {Fore.LIGHTYELLOW_EX}Gold{Style.RESET_ALL}]--")
                print("\nWhat will you buy?")
                time.sleep(1)
                shop2_buy_sword = input("\nWeapons for sale: \n"
                      f"1. Ironfang Shortsword (25 Gold, +8 Max Attack, {ironfang_stock} in stock) - A finely balanced blade forged for speed and precision.\n"
                      f"2. Runed Longsword (40 Gold, +12 Max Attack, {runed_sword_stock} in stock) - Etched with ancient runes that pulse with faint light.\n"
                      f"3. Hammer of the Deep Forge (65 Gold, +18 Max Attack, {hammer_deep_forge_stock} in stock) - Forged in the deepest caverns; each strike echoes like thunder.\n"
                      f"4. Bow of Whispering Pines (35 Gold, +10 Max Attack, {bow_whispering_pines_stock} in stock) - Its string hums with the sound of the hidden forests.\n"
                      f"5. Dagger of Shadowglass (30 Gold, +6 Max Attack, +5 Max Health, {dagger_shadowglass_stock} in stock) - A swift blade infused with shadow, sacrificing defense for speed.\n"
                      f"6. Axe of the Stonebreaker (50 Gold, +15 Max Attack, {axe_stonebreaker_stock} in stock) - Heavy and brutal, designed to cleave through armor and stone alike.\n"
                      f"7. Lance of the Eternal Guard (55 Gold, +12 Max Attack, +10 HP, {lance_eternal_guard_stock} in stock) - A balanced weapon used by the guardians of the Eternal Caverns.\n"
                      f"8. Staff of the Emberlight (45 Gold, +14 Max Attack, {staff_emberlight_stock} in stock) - A charred staff channeling a flicker of old magic.\n"
                      f"9. Crossbow of Silent Thunder (38 Gold, +11 Max Attack, {crossbow_silent_thunder_stock} in stock) - Bolts fly unseen, but strike with resounding force.\n"
                      f"10. Warblade of the Brave (75 Gold, +20 Max Attack, {warblade_brave_stock} in stock) - Legendary blade said to be wielded by the first hero of the Land of Bravery.\n"
                                        f"X. Exit Menu.\n"
                                        f"> ")
                # Player press X to Exit
                if shop2_buy_sword.strip().lower() == "x":
                    print(f"{player_name}: I, thank you, Weaponsmith for thy service.")
                    time.sleep(1)
                    shop2_weaponsmith_bye_lines()
                    time.sleep(2)
                    break
                elif shop2_buy_sword.strip() == "1" and gold >= 25:
                    if ironfang_stock > 0:
                        player_payment()
                        ironfang_stock -= 1
                        gold -= 25
                        attack_max += 8
                        shop2_player_buy_ironfang_lines()
                        time.sleep(2)
                        shop2_ironfang_shortsword_buy()
                        time.sleep(2)
                        print(f"You bought Ironfang Shortsword! +8 Max Attack. Max Attack is now {attack_max}.")
                        time.sleep(2)
                    else:
                        print("Eternal Weaponsmith: Alas, you may have forgotten what thy will get or I just dont have any of it left.")
                elif shop2_buy_sword.strip() == "2" and gold >= 40:
                    if runed_sword_stock > 0:
                        player_payment()
                        ironfang_stock -= 1
                        gold -= 40
                        attack_max += 12
                        shop2_player_buy_runesword_lines()
                        time.sleep(2)
                        shop2_runed_longsword_buy()
                        time.sleep(2)
                        print(f"You bought Runed Longsword! +12 Max Attack. Max Attack is now {attack_max}.")
                        time.sleep(2)
                    else:
                        print("Eternal Weaponsmith: Alas, you may have forgotten what thy will get or I just dont have any of it left.")
                elif shop2_buy_sword.strip() == "3" and gold >= 65:
                    if hammer_deep_forge_stock > 0:
                        player_payment()
                        hammer_deep_forge_stock -= 1
                        gold -= 65
                        attack_max += 18
                        shop2_player_buy_hammer_deep_forge_lines()
                        time.sleep(2)
                        shop2_hammer_deep_forge_buy()
                        time.sleep(2)
                        print(f"You bought Hammer of the Deep Forge! +18 Max Attack. Max Attack is now {attack_max}")
                        time.sleep(2)
                    else:
                        print("Eternal Weaponsmith: Alas, you may have forgotten what thy will get or I just dont have any of it left.")
                elif shop2_buy_sword.strip() == "4" and gold >= 35:
                    if bow_whispering_pines_stock > 0:
                        player_payment()
                        bow_whispering_pines_stock -= 1
                        gold -= 35
                        attack_max += 10
                        shop2_player_buys_bow_whispering_pines_lines()
                        time.sleep(1)
                        shop2_bow_whispering_pines_buy()
                        time.sleep(2)
                        print(f"You bought Bow of Whispering Pines! +10 Max Attack. Max Attack is now {attack_max}")
                        time.sleep(2)
                    else:
                        print("Eternal Weaponsmith: Alas, you may have forgotten what thy will get or I just dont have any of it left.")
                elif shop2_buy_sword.strip() == "5" and gold >= 30:
                    if dagger_shadowglass_stock > 0:
                        player_payment()
                        dagger_shadowglass_stock -= 1
                        gold -= 30
                        attack_max += 6
                        max_health += 5
                        shop2_player_buys_dagger_shadowglass_lines()
                        time.sleep(1)
                        shop2_dagger_shadowglass_buy()
                        time.sleep(2)
                        print(f"You bought Dagger of Shadowglass! +6 Max Attack, +5 Max HP. Max Attack is now {attack_max} & Max HP is now {max_health}.")
                        time.sleep(2)
                    else:
                        print("Eternal Weaponsmith: Alas, you may have forgotten what thy will get or I just dont have any of it left.")
                elif shop2_buy_sword.strip() == "6" and gold >= 50:
                    if axe_stonebreaker_stock > 0:
                        player_payment()
                        axe_stonebreaker_stock -= 1
                        gold -= 50
                        attack_max += 15
                        shop2_player_buys_axe_stonebreaker_lines()
                        time.sleep(1)
                        shop2_axe_stonebreaker_buy()
                        time.sleep(2)
                        print(f"You bought Axe of the Stonebreaker! +15 Max Attack. Max attack is now {attack_max}.")
                        time.sleep(2)
                    else:
                        print("Eternal Weaponsmith: Alas, you may have forgotten what thy will get or I just dont have any of it left.")
                elif shop2_buy_sword.strip() == "7" and gold >= 55:
                    if lance_eternal_guard_stock > 0:
                        player_payment()
                        lance_eternal_guard_stock -= 1
                        gold -= 55
                        attack_max += 12
                        max_health += 10
                        shop2_player_buys_lance_eternal_lines()
                        time.sleep(1)
                        shop2_lance_eternal_guard_buy()
                        time.sleep(2)
                        print(f"You bought Lance of Eternal Guard! +12 Max Attack, +10 Max HP. Max Attack is now {attack_max} & Max HP is now {max_health}.")
                        time.sleep(2)
                    else:
                        print("Eternal Weaponsmith: Alas, you may have forgotten what thy will get or I just dont have any of it left.")
                elif shop2_buy_sword.strip() == "8" and gold >= 45:
                    if staff_emberlight_stock > 0:
                        player_payment()
                        staff_emberlight_stock -= 1
                        gold -= 45
                        attack_max += 14
                        shop2_player_buys_staff_emberlight_lines()
                        time.sleep(1)
                        shop2_staff_emberlight_buy()
                        time.sleep(2)
                        print(f"You bought Staff of Emberlight! +14 Max Attack. Max Attack is now {attack_max}.")
                        time.sleep(2)
                    else:
                        print("Eternal Weaponsmith: Alas, you may have forgotten what thy will get or I just dont have any of it left.")
                elif shop2_buy_sword.strip() == "9" and gold >= 38:
                    if crossbow_silent_thunder_stock > 0:
                        player_payment()
                        crossbow_silent_thunder_stock -= 1
                        gold -= 38
                        attack_max += 11
                        shop2_player_buys_crossbow_silent_thunder_lines()
                        time.sleep(1)
                        shop2_crossbow_silent_thunder_buy()
                        time.sleep(2)
                        print(f"You bought Crossbow of the Silent thunder! +11 Max Attack. Max Attack is now {attack_max}.")
                        time.sleep(2)
                    else:
                        print("Eternal Weaponsmith: Alas, you may have forgotten what thy will get or I just dont have any of it left.")
                elif shop2_buy_sword.strip() == "10" and gold >= 75:
                    if warblade_brave_stock > 0:
                        player_payment()
                        warblade_brave_stock -= 1
                        gold -= 75
                        attack_max += 20
                        shop2_player_buys_warblade_brave_lines()
                        time.sleep(1)
                        shop2_warblade_brave_buy()
                        time.sleep(2)
                        print(f"You bought Warblade of the Brave! +20 Max Attack. Max Attack is now {attack_max}.")
                        time.sleep(2)
                    else:
                        print("Eternal Weaponsmith: Alas, you may have forgotten what thy will get or I just dont have any of it left.")
                else:
                    print("Please enter a valid option.")
        #Player goes out of the Armory
        elif shop2_move.strip() == "3":
            print(
                "You step out of the Stoneheart Armory, the scent of hot iron fading as the cool cavern air greets"
                " you once more.")
            time.sleep(3)
            break
### Chapters 1-5 ---------------------------------------------------------------------------------------------------###
# -Chapter 2-
def chapt2_eternal_caverns():
    global player_name
    print("Chapter 2: The Eternal Caverns.")
    time.sleep(1)
    print(f"\n                     --[{player_name}, {race_name} {player_class} | {Fore.RED}{player_health}{Style.RESET_ALL}/{Fore.RED}{max_health}{Style.RESET_ALL} HP | {gold} {Fore.LIGHTYELLOW_EX}Gold{Style.RESET_ALL}]--")
    skip_dialogue = input("Do you want to skip the Dialogue? (Yes/No): ").lower() == "yes"
    if not skip_dialogue:
        door_close1 = pygame.mixer.Sound(r"sounds/close door.ogg")
        door_close1.play()
        print("\nYou went out of the shop and you saw the old man signaling for you to come to his direction...")
        time.sleep(2)
        print(f"\nOld man: 'Well then {player_name}, now what the Grandmaster would like you to do is,")
        time.sleep(2)
        print("\nOld man: 'To investigate what's inside what the people would call... the Eternal Caverns.")
        time.sleep(3)
        print("\nSo you went on your way to the big hole one the side of the grassy mountain...")
        time.sleep(2)
        print("The old man then had some parting words to say,")
        time.sleep(1)
        print(f"\nOld man: 'Be careful down there, {player_name}, and once you see the light shine upon you... We'll meet again..")
        time.sleep(3)
        print("Old man: 'Go on, traveller!'")
        time.sleep(1)
        print("\nSo you went to the cave, it was dark, spacious, full of small rocks on the floor... but then!")
        time.sleep(2)
    else:
        print("You skipped the Dialogue!")
# -Chapter 3-
def chapt3_lost_trader():
    global player_name, player_health, max_health
    print("Chapter 3: Lost Trader and...bugs?")
    # Dialogue Skipping logic
    print(f"\n                              --[{player_name}, {race_name} {player_class} | {Fore.RED}{player_health}{Style.RESET_ALL}/{Fore.RED}{max_health}{Style.RESET_ALL} HP | {gold} {Fore.LIGHTYELLOW_EX}Gold{Style.RESET_ALL}]--")
    skip_dialogue = input("Do you want to skip the Dialogue? (Yes/No): ").lower() == "yes"
    if not skip_dialogue:
        print("\nYou press on deeper into the cave...")
        time.sleep(2)
        print("It was big, dense, dark with only your torch lighting up your way..")
        time.sleep(2)
        print("It smells rather rotten and stinky as if many corpses once degraded here.")
        time.sleep(2)
        print("But then suddenly, you see a glimmer of light, like there's a living being there...")
        time.sleep(2)
        print("As you walk closer to the light you see a ragged, young man and he seems like he wants to offer you something...")
        time.sleep(2)
        print("\nLost Trader: 'Greetings… Traveller, I, Silas, am once an adventurer like ye... but things have gotten... rather stale...anyways'")
        time.sleep(2)
        print("Lost Trader: 'I have some items here that might uhh... 'ease' your journey, come and take a look'")
        time.sleep(1)
    else:
        print("You skipped the Dialogue!")
    # Lost trader items
    trader_shop()
    # Spider fight Narrative
    print("You rest for a while... regaining your energy and max HP restored.")
    time.sleep(2)
    player_health = max_health  # fully heal after resting
    pygame.mixer.music.fadeout(2000)
    print("After your rest, you went on deeper to the steep part of the cave...\nSuddenly...")
    time.sleep(2)
    pygame.mixer.music.load(r"sounds/spider battle.ogg")
    pygame.mixer.music.play(-1)
    print("\nA spider creeps out from the shadows!\nThe battle begins!\n")
    # Battle Loop on Spider
    battle("Spider")
    # Narratives and healing shrine (must do sept 16, 2025)
    pygame.mixer.music.fadeout(2000)
    pygame.mixer.music.load(r"sounds/spider defeated.ogg")
    pygame.mixer.music.play(-1)
    print(f"\n                     --[{player_name}, {race_name} {player_class} | {Fore.RED}{player_health}{Style.RESET_ALL}/{Fore.RED}{max_health}{Style.RESET_ALL} HP | {gold} {Fore.LIGHTYELLOW_EX}Gold{Style.RESET_ALL}]--")
    skip_dialogue = input("Do you want to skip the Dialogue? (Yes/No): ").lower() == "yes" # If "no" the expression becomes False making the Dialogue play out
    if not skip_dialogue:
        print("A mystical light surrounds you as the Spider falls...")
        time.sleep(2)
        print(f"\nThen you remember what the old man told you earlier... 'Once you see a light shine upon ye, "f"{player_name} I'll be seeing you again..'")
        time.sleep(3)
        print("You then continued to head down the cavern, as you walk you saw a faint purple light...")
        time.sleep(2)
        print("Turns out, it was some sort of Shrine!\nSo you went near it and there was a scribble on the leg of the shrine saying,")
        time.sleep(3)
        print("'Stone of silence, carved with care'")
        time.sleep(2)
        print("'Blood and shadow vanish there'")
        time.sleep(2)
        print("'Touch, and life anew will flow,'")
        time.sleep(2)
        print("'Refuse, and onward you must go.'")
        time.sleep(2)
    else:
        print("You skipped the Dialogue!")
    print(f"\nYour current HP is {player_health}/{max_health} HP.")
    # Healing shrine code
    while True:
        choice = (input("\nWhat will you do? \n(1. Touch the shrine, 2. Walk away): "))
        if choice.strip() == "":
            print("\nPlease type down thy choice.")
        elif choice.strip() == "1":
            player_health = max_health
            print(f"The shrine healed you for {player_health}/{max_health} HP!")
            break
        elif choice.strip() == "2":
            print("You walked away and went deeper to the dark caverns...")
            break
        else:
            print("Please type a valid choice.")
    # Narrative going to poisonous spider battle
    print("\nNow you continue on your journey down deep...\nYou were walking and you hear faint screeches...")
    time.sleep(3)
    print("As if there were... bugs crawling around the area?\nBut as you were looking and wandering around in this dark cavern...")
    #  This stops by fading  the song of  the spider defeated by 2 seconds
    pygame.mixer.music.fadeout(2000)
    time.sleep(3)
    ### Poisonous  spider  battle music
    pygame.mixer.music.load(r"sounds/poison battle.mp3")
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)
    print("\nSuddenly, a poisonous spider drops from above!")
    time.sleep(1)
    # battle poisonous spider
    battle("Poisonous_Spider")
    print("The Poisonous spider drops an Enchanted Scroll...")
    time.sleep(1.7)
    print("What could be written inside it?")
    time.sleep(1.3)
    print("But before that you head on deep to the cave...")
    time.sleep(1.3)
    pygame.mixer.music.fadeout(2000)
# -Chapter 4-
def chapt4_the_last_bite():
    global player_name, player_health, max_health
    print("Chapter 4: The Last Bite, the First... Light?")
    # Narration for story...
    print(f"\n                     --[{player_name}, {race_name} {player_class} | {Fore.RED}{player_health}{Style.RESET_ALL}/{Fore.RED}{max_health}{Style.RESET_ALL} HP | {gold} {Fore.LIGHTYELLOW_EX}Gold{Style.RESET_ALL}]--")
    skip_dialogue = input("Do you want to skip the Dialogue? (Yes/No): ").lower() == "yes"
    if not skip_dialogue:
        print("\nYou celebrate your triumph! But you still have a long way to go...")
        time.sleep(3)
        print("\nAs you explore the Eternal Caverns, you found a beautiful and colorful village underground.")
        time.sleep(4)
        print("There were glowing moss and stone all round this big underground village,")
        time.sleep(3)
        print("It smelled like a chemical substance maybe spilled into this place...")
        time.sleep(3)
        print("\nThen one of the Eternal beings saw you and asked...")
        time.sleep(3)
        print("\nEternal Warrior: What brings... a human here hmm?")
        time.sleep(3)
        print("\nThen you looked at him, weirdly... I mean who wouldn't-")
        time.sleep(2)
        print("But you focused up and told him your whereabouts until you got surprised...")
        time.sleep(3)
        print(f"Eternal Being: Oh... I see, your name must be {player_name}, right?")
        time.sleep(2)
        print("\nYou took a step back, in your fighting stance...")
        time.sleep(3)
        print("\nEternal Being: Oh well dont be surprised... the old man from that, should I say, interesting village sent you here didn't he?")
        time.sleep(4)
        print("Eternal Being: Well, bad news for you human, you fell for his trap!")
        time.sleep(2)
        print("The villagers gathered around both of you, screaming and cheering!!")
        time.sleep(2)
    else:
        print("You skipped the Dialogue!")
        pygame.mixer.music.fadeout(2000)
    # Flags for the upcoming Eternal being fight
    player_health = max_health
    # Eternal warrior being fight
    pygame.mixer.music.load(r"sounds/eternal warrior.ogg")
    pygame.mixer.music.set_volume(0.7)
    pygame.mixer.music.play(-1)
    print(f"\nYou angered the Warrior of the Eternal Being! Defeat him to gain the trust of the Eternal Villagers!")
    time.sleep(3)
    battle("Eternal_Warrior")
    # The Eternal Village Introduction
    print("You stand tall against the Eternal Warrior!"
          "\nAnd gained the trust of the Eternal Warrior.")
    time.sleep(2)
    print("\nEternal Warrior: ... You're strong human, I'll be happy to help thee with whatever thy need.")
    time.sleep(3)
    print("You looked around and all the Eternal Villagers were cautious but clapping for you!")
    time.sleep(3)
    # Player responds to eternal warrior
    player_eternal_warrior_talking()

# SHop 1 name of shopkeepers
shop1_names = [
    "\nBethwyn, the Shopkeeper",
    "\nMarigwen, the Shopkeeper",
    "\nRowena, the Shopkeeper",
    "\nGwyneira, the Shopkeeper",
    "\nLiora, the Shopkeeper",
    "\nSerilda, the Shopkeeper",
    "\nFaylinn, the Shopkeeper",
    "\nHestara, the Shopkeeper",
    "\nEldrine, the Shopkeeper",
    "\nMorwenna, the Shopkeeper",
    "\nSelitha, the Shopkeeper",
    "\nBranwyn, the Shopkeeper",
    "\nTamsin, the Shopkeeper",
    "\nIsolde, the Shopkeeper",
    "\nVelmara, the Shopkeeper",
    "\nNerissa, the Shopkeeper",
    "\nAmariel, the Shopkeeper",
    "\nCelandine, the Shopkeeper",
    "\nYsolde, the Shopkeeper",
    "\nOdelia, the Shopkeeper",
    "\nAida, the Shopkeeper"

]
def shop1_shopkeepers():
    print(random.choice(shop1_names))
# Shopkeeper lines
beth_lines = [

    "\nShopkeeper: Ah, traveller! Step right in. My shelves groan with goods rarer than dragon's teeth.",
    "\nShopkeeper: Coin speaks louder than oaths here — but I do fancy a good story if you've one to trade.",
    "\nShopkeeper: Mind your boots on my rushes, stranger. Mud's harder to sweep than goblin bones.",
    "\nShopkeeper: These potions? Brewed at dawn, stirred 'til dusk. Won't find fresher 'less you raid a witch's hut.",
    "\nShopkeeper: Gold upfront, no IOUs. I've learned that lesson harder than a blacksmith's hammer.",
    "\nShopkeeper: Take your time — I've got till sunset… unless the guards call curfew again.",
    "\nShopkeeper: A bargain? Hah! You'll get a fair price, but my cat still needs feeding.",
    "\nShopkeeper: You look half-dead. Buy a Potion before you collapse and ruin my floor.",
    "\nShopkeeper: We've got travelers from the East, sellswords from the North… but none as curious as you.",
    "\nShopkeeper: Come back if you live through your quest. I'll still be here, counting coins and gossip."

]
def beth_talks():
        print(random.choice(beth_lines))
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
# Eternal Bartender not enough gold lines lol
tavern_no_gold = [

    "\nEternal Barkeeper: Ho there, traveler! Thy purse be empty, and my casks not for charity.",
    "\nEternal Barkeeper: Thou canst not buy that with naught but lint and air… nor from an empty barrel.",
    "\nEternal Barkeeper: 'Hah! Do ye fancy taking wares without paying? Or from shelves already bare?'",
    "\nEternal Barkeeper: 'Thy pockets be as light as a feather, and my stock as dry as a monk’s cellar.'",
    "\nEternal Barkeeper: 'Nay, friend. The coin is wanting, and so too the drink thou seekest.'",
    "\nEternal Barkeeper: 'Fie! Thou wouldst rob me with thine empty purse? Best return with coin — and hope my stock be full.'",
    "\nEternal Barkeeper: 'The shelves be bare, and thy gold is naught. Come again when fortune and barrels be fuller.'",
    "\nEternal Barkeeper: 'By my wares, thy coin falls short, and so too doth my supply. Fate be fickle this day.'",
    "\nEternal Barkeeper: 'Thou hast not the means, and I not the drink. These goods require more than thy pockets yield.'",
    "\nEternal Barkeeper: 'Gold lacking, barrels empty — good traveler, only patience may serve thee now.'"

]
def no_gold_tavern():
    print(random.choice(tavern_no_gold))
# Stoneheart Armorer greeting lines
shop2_lines = [

    "\nStoneheart Armorer: 'Step in, traveler—walls of steel I sell, not toys of war.'",
    "\nStoneheart Armorer: 'Armor aplenty, strong as the cavern stone. Let us see what shall keep thee standing.'",
    "\nStoneheart Armorer: 'Blades win battles, aye, but armor keeps thee breathing. What shall it be?'",
    "\nStoneheart Armorer: 'Welcome, wanderer. Choose wisely, for a weak blade in these halls spells thy doom.'",
    "\nStoneheart Armorer: 'Every weapon here hath felt the stone fires. Shall one now taste thy hand?'",
    "\nStoneheart Armorer: 'Steel, iron, and a touch of enchantment—pick thy defense, and walk safe 'mong shadows.'",
    "\nStoneheart Armorer: 'A good sword sings, yet a shield whispers safety. What song pleaseth thee this day?'",
    "\nStoneheart Armorer: 'Not all who wander these caverns return. Fortify thyself, noble one, fortify thyself.'",
    "\nStoneheart Armorer: 'Each piece I forge hath a tale of grit and flame. Which tale shalt thou wear?'",
    "\nStoneheart Armorer: 'Step closer, brave soul. Even the smallest dagger may turn the tide of fate.'"

]
def shop2_armorer():
    print(random.choice(shop2_lines))
# Stoneheart Armorer when player buys Armor:
shop2_armor_lines = [

    "\nEternal Armorer: 'Hail, good traveler! Welcome to Stoneheart armory, where steel and courage are wrought alike.'",
    "\nEternal Armorer: 'Seekest thou a cuirass? This Breastplate hath shielded knights in many a dark encounter.'",
    "\nEternal Armorer: 'Mark me well, this chainmail is light of weight, yet stout against the sharpest of blades.'",
    "\nEternal Armorer: 'Ah, thou hast an eye for quality. This helm shall guard thy head as if by ancient enchantment.'",
    "\nEternal Armorer: 'Take heed, these gauntlets are forged for both battle and craft.'",
    "\nEternal Armorer: 'A cloack of hardened hide? A wise choice, for it shall keep thee both hidden and unarmed.'",
    "\nEternal Armorer: 'Guard thy feet with these boots, for the caverns' stones bite the unwary traveler sorely.'",
    "\nEternal Armorer: 'Thou hast chosen well, brave soul. With this armor, none shall lightly best thee in combat.'",
    "\nEternal Armorer: 'Steel is thine ally, but remember: valor and wits shall serve thee even more in this dark halls.'",
    "\nEternal Armorer: 'Go forth with courage, knight, or adventurer. May thy armor endure, and thy tale be sung in ages hence'"

]
def shop2_armorer_visit():
    print(random.choice(shop2_armor_lines))
# Stoneheart Armorer when player buys the Steel Cuirass
steel_cuirass_lines = [

    "\nEternal Armorer: 'Ah, the Steel Cuirass! Worn by the bravest of knights, it shall guard thy heart and soul.'",
    "\nEternal Armorer: 'Feel the weight of courage upon thy chest, adventurer.'",
    "\nEternal Armorer: 'This cuirass hath withstood countless blows; may it serve thee well in battle.'",
    "\nEternal Armorer: 'A fine choice! Let no blade pierce thy resolve.'",
    "\nEternal Armorer: 'Wear it with pride, for many tales shall be sung of thy valor.'"

]
def shop2_cuirass_buy():
    print(random.choice(steel_cuirass_lines))
# Stoneheart Armorer when player buys the Chainmail Hauberk
chainmail_hauberk_lines = [

    "\nEternal Armorer: 'The hauberk is light, yet strong; thou shalt move swift whilst shielded.'",
    "\nEternal Armorer: 'Chain by chain, it binds protection to thee.'",
    "\nEternal Armorer: 'Many a foe hath met their match against this fine mail.'",
    "\nEternal Armorer: 'Let no sharp edge find thy flesh whilst clad in this.'",
    "\nEternal Armorer: 'A splendid choice! May it keep thee safe in darkest halls.'"
]
def shop2_hauberk_buy():
    print(random.choice(chainmail_hauberk_lines))
# Stoneheart Armorer when player buys the Knight's Helm
knight_helm_lines = [

    "Eternal Armorer: 'This helm shall guard thy mind and skull alike.'",
    "Eternal Armorer: 'Many a hero's head hath been saved by such craftsmanship.'",
    "Eternal Armorer: 'Wear it boldly, for it bears the mark of the eternal forge.'",
    "Eternal Armorer: 'A wise choice, for a sharp mind must have a safe head.'",
    "Eternal Armorer: 'May this helm shine as brightly as thy courage in battle.'"
]
def shop2_helm_buy():
    print(random.choice(knight_helm_lines))
# Stoneheart Armorer when player buys Gauntlets of Grip
gauntlets_grip_lines = [

    "Eternal Armorer: 'These gauntlets shall make thy strikes true and fierce.'",
    "Eternal Armorer: 'Grip thy weapon, and let none stand before thee.'",
    "Eternal Armorer: 'Forged for strength, they shall augment thy power in battle.'",
    "Eternal Armorer: 'Feel the might of the forge in thy fists, adventurer.'",
    "Eternal Armorer: 'A wise choice! Let thy enemies tremble at thy touch.'"
]
def shop2_gauntlets_grip_buy():
    print(random.choice(gauntlets_grip_lines))
# Stoneheart Armorer when player buys Reinforced Hide Cloak
reinforced_hide_cloak_lines = [

    "Eternal Armorer: 'This helm shall guard thy mind and skull alike.'",
    "Eternal Armorer: 'Many a hero's head hath been saved by such craftsmanship.'",
    "Eternal Armorer: 'Wear it boldly, for it bears the mark of the eternal forge.'",
    "Eternal Armorer: 'A wise choice, for a sharp mind must have a safe head.'",
    "Eternal Armorer: 'May this helm shine as brightly as thy courage in battle.'"
]
def shop2_reinforced_hide_cloak_buy():
    print(random.choice(reinforced_hide_cloak_lines))
# Stoneheart Armorer when player buys Boots of Stoneguard
boots_of_stoneguard_lines = [

    "Eternal Armorer: 'These boots shall steady thy steps upon treacherous paths.'",
    "Eternal Armorer: 'Feel the earth beneath thee, guarded with every stride.'",
    "Eternal Armorer: 'Many a cavern traveler hath owed their life to these boots.'",
    "Eternal Armorer: 'Step boldly, adventurer, the stones shall not betray thee.'",
    "Eternal Armorer: 'Wear them well; let not the ground undo thy courage.'"
]
def shop2_boots_of_stoneguard_buy():
    print(random.choice(boots_of_stoneguard_lines))
# Stoneheart Armorer when player buys Pauldrons of Valor
pauldrons_of_valor_lines = [

    "Eternal Armorer: 'These pauldrons shall lend force to every swing of thy blade.'",
    "Eternal Armorer: 'Shoulder the might of heroes past with these crafted arms.'",
    "Eternal Armorer: 'A fine choice! Strike true and strike hard.'",
    "Eternal Armorer: 'Let thy enemies feel the weight of thy valor.'",
    "Eternal Armorer: 'May these pauldrons turn aside foes as easily as they turn heads in awe.'"
]
def shop2_pauldrons_of_valor_buy():
    print(random.choice(pauldrons_of_valor_lines))
# Stoneheart Armorer when player buys Bracers of Fortitude
bracers_of_fortitude_lines = [

    "Eternal Armorer: 'These bracers shall protect thy arms and bolster thy spirit.'",
    "Eternal Armorer: 'A wise choice, adventurer; defense begins at thy forearms.'",
    "Eternal Armorer: 'Feel the steady strength of the forge in every movement.'",
    "Eternal Armorer: 'Fortify thyself; let no strike shake thy resolve.'",
    "Eternal Armorer: 'May these bracers guard thee well in all thy battles.'"
]
def shop2_bracers_of_fortitude_buy():
    print(random.choice(bracers_of_fortitude_lines))
# Stoneheart Armorer when player buys Gorget of the Brave
gorget_of_the_brave_lines = [

    "Eternal Armorer: 'Protect thy throat, brave soul, for it speaks words that may save lives.'",
    "Eternal Armorer: 'This gorget shields both flesh and courage.'",
    "Eternal Armorer: 'Wear it boldly; danger shall glance off its steel.'",
    "Eternal Armorer: 'May it remind thee always of thy bravery.'",
    "Eternal Armorer: 'A small piece, but mighty in defense; thou hast chosen wisely.'"
]
def shop2_gorget_of_the_brave_buy():
    print(random.choice(gorget_of_the_brave_lines))
# Stoneheart Armorer when player buys Shield of the Eternal Caverns
shield_of_eternal_caverns_lines = [

    "Eternal Armorer: 'A shield of legends! Let no foe breach thy guard.'",
    "Eternal Armorer: 'Many a cavern warrior hath trusted this shield with their life.'",
    "Eternal Armorer: 'Raise it high and let it turn aside all harm.'",
    "Eternal Armorer: 'With this in hand, thou art a fortress unto thyself.'",
    "Eternal Armorer: 'May thy courage match the unyielding stone of this shield.'"

]
def shop2_shield_of_eternal_caverns_buy():
    print(random.choice(shield_of_eternal_caverns_lines))
# Stoneheart Armorer says farewell
stoneheart_armorer_bye =[

    "Eternal Armorer: 'Go forth, traveler, and may steel and courage never fail thee.'",
    "Eternal Armorer: 'The caverns watch over thee — return shouldst thou need mending or more steel.'",
    "Eternal Armorer: 'Step with care, for shadows grow deep and foes grow bold.'",
    "Eternal Armorer: 'May thy armor bear thee through many battles, and thy name echo in the halls of heroes.'",
    "Eternal Armorer: 'Farewell, brave soul — the Stoneheart Armory awaits thy next venture.'"
]
def shop2_stoneheart_armorer_bye():
    print(random.choice(stoneheart_armorer_bye))
# Stoneheart Weaponsmith
stoneheart_weaponsmith_greetings = [

    "Eternal Weaponsmith: 'Ah, a wanderer seeking steel. Step forth and see Stoneheart's craft!'",
    "Eternal Weaponsmith: 'Welcome, traveller. Here iron breathes fire and remembers battle.'",
    "Eternal Weaponsmith: 'The forge still glows. What weapon shall be thy companion?'",
    "Eternal Weaponsmith: 'Hail, bold soul. These blades thirst for a legend to wield them.'",
    "Eternal Weaponsmith: 'Enter the forge, where sparks dance and weapons gain true names.'",
    "Eternal Weaponsmith: 'I smell battle on thee. Choose thy edge or hammer wisely.'",
    "Eternal Weaponsmith: 'Stoneheart's weapons have ended tyrants and beasts alike.'",
    "Eternal Weaponsmith: 'Good steel, fair price. Step closer and see what suits thy grip.'",
    "Eternal Weaponsmith: 'No trinkets here, only true weapons of war.'",
    "Eternal Weaponsmith: 'Welcome back, adventurer. The blades wait for steady hands.'"

]
def shop2_weaponsmith_greetings():
    print(random.choice(stoneheart_weaponsmith_greetings))
# Stoneheart Weapons bought
ironfang_shortsword_buy_lines = [

    "Eternal Weaponsmith: A nimble blade for a swift hand—use it well.",
    "Eternal Weaponsmith: Ah, speed and precision! This will suit you perfectly.",
    "Eternal Weaponsmith: May your strikes be as sharp as this ironfang.",
    "Eternal Weaponsmith: A fine choice for those who value agility over brute force.",
    "Eternal Weaponsmith: Handle it with care; its balance is delicate but deadly."
]
def shop2_ironfang_shortsword_buy():
    print(random.choice(ironfang_shortsword_buy_lines))
runed_longsword_buy_lines = [

    "Eternal Weaponsmith: The runes will guide your hand in battle—choose wisely.",
    "Eternal Weaponsmith: An ancient blade for one with courage in their heart.",
    "Eternal Weaponsmith: Let its light illuminate your path and your foes' defeat.",
    "Eternal Weaponsmith: Ah, a weapon with history and magic intertwined!",
    "Eternal Weaponsmith: Wield it with honor; it has seen battles long past."
]
def shop2_runed_longsword_buy():
    print(random.choice(runed_longsword_buy_lines))
hammer_deep_forge_buy_lines = [

    "Eternal Weaponsmith: May its strikes shake the very earth beneath your foes!",
    "Eternal Weaponsmith: Ah, the hammer that roars with the deep caverns' fury.",
    "Eternal Weaponsmith: Heavy, brutal, and true—just like its wielder must be.",
    "Eternal Weaponsmith: Let its echo warn your enemies before they even see you.",
    "Eternal Weaponsmith: A mighty choice! Few can handle such power with skill."
]
def shop2_hammer_deep_forge_buy():
    print(random.choice(hammer_deep_forge_buy_lines))
bow_whispering_pines_buy_lines = [

    "Eternal Weaponsmith: Listen to the forest as it guides your arrow true.",
    "Eternal Weaponsmith: Silent but deadly, just like the shadows between the trees.",
    "Eternal Weaponsmith: Ah, a bow for a keen eye and a steady hand.",
    "Eternal Weaponsmith: May your aim be as true as the whispers of the pines.",
    "Eternal Weaponsmith: A weapon that strikes unseen—your foes won’t know what hit them."
]
def shop2_bow_whispering_pines_buy():
    print(random.choice(bow_whispering_pines_buy_lines))
dagger_shadowglass_buy_lines = [

    "Eternal Weaponsmith: Swift, silent, and sharp—perfect for the cunning adventurer.",
    "Eternal Weaponsmith: A dagger that blends with the shadows. Use wisely.",
    "Eternal Weaponsmith: Speed over defense, but a master’s hand can make it lethal.",
    "Eternal Weaponsmith: May this blade slip through defenses as easily as it slips through darkness.",
    "Eternal Weaponsmith: A choice for those who strike first and vanish without a trace."
]
def shop2_dagger_shadowglass_buy():
    print(random.choice(dagger_shadowglass_buy_lines))
axe_stonebreaker_buy_lines = [

    "Eternal Weaponsmith: Heavy and unforgiving, just like true strength should be.",
    "Eternal Weaponsmith: An axe to split armor and shatter stone—excellent pick!",
    "Eternal Weaponsmith: May your enemies feel the weight of your resolve.",
    "Eternal Weaponsmith: Brutal but precise—handle with might and care.",
    "Eternal Weaponsmith: Ah, a weapon for those who face challenges head-on!"
]
def shop2_axe_stonebreaker_buy():
    print(random.choice(axe_stonebreaker_buy_lines))
lance_eternal_guard_buy_lines = [

    "Eternal Weaponsmith: A weapon of guardians—carry its honor well.",
    "Eternal Weaponsmith: Balanced and true, perfect for a steadfast adventurer.",
    "Eternal Weaponsmith: May this lance protect you as much as it pierces your foes.",
    "Eternal Weaponsmith: Wield it with courage; legends were made with such weapons.",
    "Eternal Weaponsmith: An eternal choice for one destined for greatness."
]
def shop2_lance_eternal_guard_buy():
    print(random.choice(lance_eternal_guard_buy_lines))
staff_emberlight_buy_lines = [

    "Eternal Weaponsmith: A spark of old magic now in your hands—use it wisely.",
    "Eternal Weaponsmith: Its flicker may light your path or your enemies’ end.",
    "Eternal Weaponsmith: Channel its power carefully; magic is as temperamental as flame.",
    "Eternal Weaponsmith: Ah, a staff that burns with knowledge and strength.",
    "Eternal Weaponsmith: May your enemies feel the warmth of your resolve!"
]
def shop2_staff_emberlight_buy():
    print(random.choice(staff_emberlight_buy_lines))
crossbow_silent_thunder_buy_lines = [
    "Eternal Weaponsmith: Silent but deadly, like a storm waiting to strike.",
    "Eternal Weaponsmith: Your enemies won’t hear it coming, only the aftermath.",
    "Eternal Weaponsmith: A precise and deadly choice for one with a sharp eye.",
    "Eternal Weaponsmith: May your bolts fly true and your aim never ogger.",
    "Eternal Weaponsmith: Ah, a weapon that speaks louder than words."
]
def shop2_crossbow_silent_thunder_buy():
    print(random.choice(crossbow_silent_thunder_buy_lines))
warblade_brave_buy_lines = [
    "Eternal Weaponsmith: A legendary blade for a bold heart—use it wisely!",
    "Eternal Weaponsmith: Wield it with courage, and your name may join the heroes of old.",
    "Eternal Weaponsmith: Its edge was forged for those who dare greatly.",
    "Eternal Weaponsmith: May this blade carry you to glory and honor.",
    "Eternal Weaponsmith: Ah, the first hero’s weapon! Handle with pride and strength."
]
def shop2_warblade_brave_buy():
    print(random.choice(warblade_brave_buy_lines))
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
# Loreweaver greets player
loreweaver_greets = [
    "Loreweaver: Ah… a traveler steps through my door. The Caverns whisper your tale already.",
    "Loreweaver: Welcome, seeker. These shelves hold the stories of both the living… and the forgotten.",
    "Loreweaver: Sit, child of the surface. The Eternal Village has waited long for a listener.",
    "Loreweaver: The threads of fate tremble around you, as though your arrival was written in ancient ink.",
    "Loreweaver: Shh… listen. Can you hear it? The Caverns themselves hum with your destiny."
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

    "Loreweaver: Go with care, traveler. The threads of fate are never idle.",
    "Loreweaver: May the stories guide your steps… until we meet again.",
    "Loreweaver: Walk carefully, for the world is full of tales both light and dark.",
    "Loreweaver: Return safely, and bring with you the whispers of your journey.",
    "Loreweaver: The scrolls will wait, but time does not. Farewell for now.",
    "Loreweaver: Step lightly, seeker. Your story is only beginning."
]
def loreweaver_farewell_lines():
    print(random.choice(loreweaver_farewell))
# Echo Binder greets the player
echo_binder_greetings = [
    "Echo-Binder: Welcome, traveler… every drop here carries a memory, every vial an echo of power.",
    "Echo-Binder: Step softly — the potions are awake and listening.",
    "Echo-Binder: Ah, a seeker of tinctures and truths… what essence shall I bind for you today?",
    "Echo-Binder: The caverns whisper your ailments before you speak. I have a remedy waiting.",
    "Echo-Binder: Careful with your hands, stranger; even my shadows are steeped in alchemy.",
    "Echo-Binder: Welcome to Echoing Vials — where whispers become draughts, and draughts become destiny."
]
def echo_binder_greetings_lines():
    print(random.choice(echo_binder_greetings))
# Echo Binder showing the player the menu
echo_binder_menu = [
    "\nEcho-Binder: Ah, greetings, weary traveler! Care for a draught that whispers secrets or one that merely tickles the nose?",
    "\nEcho-Binder: Step right in! I’ve brewed concoctions that’ll make your boots dance… or at least your tongue.",
    "\nEcho-Binder: By the moon’s light! Our vials hold more than potion—sometimes a bit of mischief as well.",
    "\nEcho-Binder: Hail, adventurer! Choose wisely, for some of these brews might sing… and others might snore.",
    "\nEcho-Binder: Welcome, bold one! These elixirs may heal, may charm, or may cause your hat to grow three sizes.",
    "\nEcho-Binder: Ah, a curious soul! Perchance you fancy a sip that soothes, or one that makes you question reality—either’s on the menu."
]
def echo_binder_menu_lines():
    print(random.choice(echo_binder_menu))
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
# Player rests Etenal Sanctuary
player_sleeps = [
    "You rest within the Eternal Sanctuary, where even time itself seems to sleep. Your wounds fade, and your spirit feels renewed.",
    "The warmth of candlelight and soft hymns cradle your weary soul. You drift into a dreamless rest…",
    "You hand over the coins and settle into your chamber. The Eternal Sanctuary’s tranquil air mends both flesh and spirit.",
    "You rent a room within the Eternal Sanctuary. The silence is deep — the kind that heals.",
    "The chamber hums faintly with the pulse of ancient wards. As you close your eyes, the Sanctuary itself seems to breathe life back into you.",
    "You lie upon sanctified linens woven with threads of moonlight. When you wake, you feel as though touched by the divine."
]
def player_sleeping():
    print(random.choice(player_sleeps))
# Soulwarden says bye to player
def soulwarden_farwell():
    global player_name
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
# Echokeeper farewell to the player when they leave Rift of Echoing Souls
echokeeper_farewell = [
    "Echokeeper: 'The echoes fade... yet your soul still hums with their memory. Rest well, wanderer.'",
    "Echokeeper: 'You return from the Rift untouched — or perhaps... changed in ways unseen.'",
    "Echokeeper: 'Every battle leaves a mark, not upon the flesh, but the spirit. Do not ignore its whisper.'",
    "Echokeeper: 'The Rift remembers you now. Its gaze will follow until you return again.'",
    "Echokeeper: 'You’ve faced what stirs in the dark between worlds. Few ever return so composed.'",
    "Echokeeper: 'Do not linger too long in peace — the echoes grow restless when forgotten.'",
    "Echokeeper: 'Well fought. The Rift bends to no one, yet it seems to respect your courage.'",
    "Echokeeper: 'Leave now, before the Rift grows curious once more. It has a hunger for familiar souls.'"
]
def echokeeper_farewell_lines():
    print(random.choice(echokeeper_farewell))
# Eternal sacntuary restaurant
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
# Rift of Echoing Souls level 1 dialogue
eternal_arena_lvl_1 = [
    "You step into the first layer of the Rift — the air hums with forgotten echoes."
    "A dim mist coils around your feet as faint whispers call your name from beyond."
    "The stone floor trembles softly — something stirs within the gloom ahead..."
    "The Rift welcomes you, softly — as though it knows you will not last long."
]
def eternal_arena_lvl1():
    print(random.choice(eternal_arena_lvl_1))
# Rift of  echoing Souls level 2 dialogue
eternal_arena_lvl_2 = [
    "The ground cracks beneath each step; shadows shift where light dares not linger."
    "A deep rumble rolls through the cavern — something vast awakens below."
    "You breathe in the dust of long-forgotten warriors — the Rift remembers them all."
    "Flames flicker from unseen braziers, as if the Rift itself is watching your every move."

]
def eternal_arena_lvl2():
    print(random.choice(eternal_arena_lvl_2))
# Rift of Echoing Souls level 3 Dialogue
eternal_arena_lvl_3 = [
    "The air grows colder, heavier — the walls pulse faintly like a living heart."
    "Every echo of your footstep comes back wrong — twisted, delayed, almost mocking."
    "A faint melody hums through the stones... no, not a melody — a lament."
    "The Rift deepens around you — it feels as though time itself bends in this place."
]
def eternal_arena_lvl3():
    print(random.choice(eternal_arena_lvl_3))
# Rift of Echoing Souls level 4 dialogue
eternal_arena_lvl_4 = [
    "You descend into the Reverberant Abyss — where even echoes refuse to speak."
    "The ground bleeds faint light as ancient runes awaken beneath your feet."
    "You sense it — something watching, something vast and hateful, smiling unseen."
    "The Rift hums violently, as though angry that you’ve come this far."
]
def eternal_arena_lvl4():
    print(random.choice(eternal_arena_lvl_4))
# Rift of Echoing Souls level 5 dialgoue
eternal_arena_lvl_5 = [
    "You stand at the heart of the Rift — where souls go not to die, but to remember."
    "The walls shimmer with trapped spirits, their forms flickering like candlelight."
    "Every breath feels borrowed. Every heartbeat, a trespass."
    "The Rift opens before you — vast, endless, and hungry. You walk forward anyway."
]
def eternal_arena_lvl5():
    print(random.choice(eternal_arena_lvl_5))
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
# Game title & music--------------------------------------------------------------------------------------------------------------------------------------#
pygame.mixer.music.load(land_of_bravery_bgm)
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)
print("                                                                             ------------------------------------")
print(Style.BRIGHT + Fore.LIGHTMAGENTA_EX + "                                                                             === Quest of the Eternal Caverns ===")
print("                                                                             ------------------------------------")
time.sleep(1)
print(Style.BRIGHT + Fore.GREEN + "\nChapter 1: The Land of Bravery.")
print("\nThe Land of Bravery unfolds before you — rolling fields under a soft sun, breeze carrying the scent of wildflowers and distant forge-fire.")
time.sleep(1)
print("Villagers bustle between cottages and markets, laughter mixing with the clang of hammers.")
time.sleep(1)
print("Banners of the Eternal King flutter above watchtowers, promising protection yet whispering of mysteries still untold.")
time.sleep(1)

# Game adds quest to the player's quest list
add_quest(player_quests, "Welcome to the Land of Bravery!", "Walk through the Land of Bravery and introduce yourself.")
# Player skips dialogue (get asked)
skip_dialogue = input("\nDo you want to skip the Dialogue? (Yes/No): ").lower() == "yes"
# intro narration
if not skip_dialogue:
    print("One sunny day, you decided to go on an adventure by yourself... and you stumbled upon the Land of Bravery!")
    time.sleep(3)
    print("The land was filled with friendly, busy, warm and welcoming yet strange villagers.")
    time.sleep(3)
    print("On the right, you were seeing blacksmiths hard at work, crafting the tools the workers need,")
    time.sleep(3)
    print("On the left, you see villagers talking to each other, laughing , and the others gathering wheat for their food,")
    time.sleep(4)
    print("Around you hear the whole village's noise, kids playing here and there...")
    time.sleep(3)
    print("As you wander around, you saw a big hole on the side of the neighboring mountain... you got curious... but,")
    time.sleep(3)
    print("\nThen you were approached by an old man in the village...")
    time.sleep(2)
    old_man_greet = pygame.mixer.Sound(r"sounds/old man.ogg")
    old_man_greet.play()
    time.sleep(0.5)
    print("\nOld Man: Greetings traveller, are ye brave enough to step foot in our land?")
    time.sleep(2)
    print("\nYou were shaken and surprised, but you regained your composure...")
    time.sleep(1)
else:
    print("You skipped the Dialogue!")
# response condition, if they say yes continue if no then get out!
response = input("\nOld Man: Are you ready to embark on your journey, traveller? Yes or No: ")
if response.lower() == "yes":
    print("\nOld Man: Now if I may ask...")
    time.sleep(1)
else:
    print("\nOld Man: Be gone! You are not worthy to fight for our land you coward!")
    exit()
# Ask for player name
player_name = input("\nOld Man: What is thy name, traveller?: ").strip()
while player_name == "":
    print("Old Man: I know you have the ability speak, traveller.")
    player_name = input("\nOld Man: What is thy name, traveller? ").strip()
######## Player random lines:
# IRONFANG PLAYER BUY LINES
player_buys_ironfang_lines = [

    f"{player_name}: I shall take this swift blade, master Eternal.\"",
    f"{player_name}: This sword is nimble, I shall wield it well.\"",
    f"{player_name}: By my hand, it shall strike true and fast.\"",
    f"{player_name}: I claim this blade for my travels ahead.\"",
    f"{player_name}: A fine sword! I shall put it to good use.\""
]
def shop2_player_buy_ironfang_lines():
    print(random.choice(player_buys_ironfang_lines))
# RUNESWORD PLAYER BUY LINES
player_buys_runesword_lines = [

    f"{player_name}: These runes call to me, I shall take it.",
    f"{player_name}: I shall wield this ancient sword with honor.",
    f"{player_name}: By its magic, I hope to strike wisely.",
    f"{player_name}: I claim this blade for my quests.",
    f"{player_name}: May this sword guide my hand in battle."
]
def shop2_player_buy_runesword_lines():
    print(random.choice(player_buys_runesword_lines))
# HAMMER OF THE DEEP FORGE PLAYER BUY LINES
player_buys_hammer_deep_forge_lines = [
    f"{player_name}: This mighty hammer shall be mine.",
    f"{player_name}: I shall crush my foes with this, Eternal.",
    f"{player_name}: By my strength, this hammer shall serve me well.",
    f"{player_name}: I claim this weapon of thunder and stone.",
    f"{player_name}: With this, no armor shall withstand me."
]
def shop2_player_buy_hammer_deep_forge_lines():
    print(random.choice(player_buys_hammer_deep_forge_lines))
# BOW WHISPERING PINES PLAYER BUY LINES
player_buys_bow_whispering_pines_lines = [

    f"{player_name}: I shall take this bow and let the forest guide me.",
    f"{player_name}: Silent and true, I shall strike unseen.",
    f"{player_name}: By the pines, my aim shall not falter.",
    f"{player_name}: I claim this bow for swift justice.",
    f"{player_name}: My arrows shall fly as whispers through the trees."
]
def shop2_player_buys_bow_whispering_pines_lines():
    print(random.choice(player_buys_bow_whispering_pines_lines))
# DAGGER OF THE SHADOWGLASS PLAYER BUY LINES
player_buys_dagger_shadowglass_lines = [

    f"{player_name}: I shall wield this dagger from shadow and mist.",
    f"{player_name}: Quick and silent, it shall serve me well.",
    f"{player_name}: By cunning and speed, I shall strike true.",
    f"{player_name}: I claim this blade for secret deeds.",
    f"{player_name}: Shadows shall hide my hand, yet my strike will be deadly."
]
def shop2_player_buys_dagger_shadowglass_lines():
    print(random.choice(player_buys_dagger_shadowglass_lines))
# AXE STONEBREAKER PLAYER BUY LINES
player_buys_axe_stonebreaker_lines = [

    f"{player_name}: This axe shall rend both stone and foe.",
    f"{player_name}: I claim this mighty weapon for my battles.",
    f"{player_name}: By my strength, none shall stand before me.",
    f"{player_name}: A weapon of power! I shall wield it well.",
    f"{player_name}: Let the stones break beneath its swing."
]
def shop2_player_buys_axe_stonebreaker_lines():
    print(random.choice(player_buys_axe_stonebreaker_lines))
# LANCE OF THE ETERNAL GUARD PLAYER BUY LINES
player_buys_lance_eternal_lines = [
    f"{player_name}: I shall wield this lance with honor and courage.",
    f"{player_name}: By the Eternal Guard, I claim this weapon.",
    f"{player_name}: Steady and true, it shall guide my hand.",
    f"{player_name}: I shall ride forth with this lance in valor.",
    f"{player_name}: Let this lance serve me in noble deeds."
]
def shop2_player_buys_lance_eternal_lines():
    print(random.choice(player_buys_lance_eternal_lines))
# STAFF OF EMBERLIGHT PLAYER BUY LINES
player_buys_staff_emberlight_lines = [

    f"{player_name}: I claim this staff, bearer of ember and flame.",
    f"{player_name}: By its magic, I shall light the darkness.",
    f"{player_name}: I shall wield its fire with wisdom and care.",
    f"{player_name}: Let the ember guide my hand in battle.",
    f"{player_name}: This staff shall serve me well on my quest."

]
def shop2_player_buys_staff_emberlight_lines():
    print(random.choice(player_buys_staff_emberlight_lines))
# CROSSBOW OF SILENT THUNDER PLAYER BUY LINES
player_buys_crossbow_silent_thunder_lines = [

    f"{player_name}: I shall take this crossbow, silent as the storm.",
    f"{player_name}: My enemies shall hear naught, yet fall swiftly.",
    f"{player_name}: I claim this weapon to strike from afar.",
    f"{player_name}: Each bolt shall fly true and sure.",
    f"{player_name}: By thunder and silence, I shall prevail."
]
def shop2_player_buys_crossbow_silent_thunder_lines():
    print(random.choice(player_buys_crossbow_silent_thunder_lines))
# WARBLADE OF THE BRAVE PLAYER BUY LINES
player_buys_warblade_brave_lines = [
    f"{player_name}: I shall wield this legendary blade with courage.",
    f"{player_name}: May my deeds honor this sword.",
    f"{player_name}: I claim this weapon for battles yet to come.",
    f"{player_name}: With this warblade, I shall carve my name in legend.",
    f"{player_name}: By bravery, I shall master this mighty sword."

]
def shop2_player_buys_warblade_brave_lines():
    print(random.choice(player_buys_warblade_brave_lines))
# Stoneheart weaponsmith says farewell to the player
shop2_weaponsmith_farewell = [

    "Eternal Weaponsmith: Fare thee well, adventurer. May your blade strike true!",
    "Eternal Weaponsmith: Go forth with courage, and return safe from your quests.",
    "Eternal Weaponsmith: May fortune and skill follow you on your journey.",
    "Eternal Weaponsmith: Keep your wits sharp and your sword sharper.",
    "Eternal Weaponsmith: Until next time, may your path be free of shadows."
]
def shop2_weaponsmith_bye_lines():
    print(random.choice(shop2_weaponsmith_farewell))
# THREAD OF FATE RANDOM LINES FOR PLAYER
thread_of_fate_lines =[
    f"“A shadow travels beside you {player_name}, but only in darkness will it reveal its true face.”",
    "“Your hands will heal what your blade cannot strike — yet the cost will weigh heavy.”",
    "“A blossom of ember burns in the deep; its glow will either save or doom you.”",
    "“The old one’s path winds like a serpent; beware the bite at the journey’s end.”",
    "“A forgotten ally waits beneath stone and echo, loyal only to the brave.”",
    "“Fate twists your name into two endings — only one hand will guide it.”",
    "“The cavern will echo your scream or your triumph; the choice is not yet made.”",
    "“You will drink from a silver cup and learn it carries both poison and power.”",
    "“An ancient door sealed by sorrow will open at your touch — and you will not walk away unchanged.”",
    "“In the darkest passage, you’ll find a light that is not your own — follow or be swallowed.”"
]
def thread_of_fate():
    print(random.choice(thread_of_fate_lines))
## ------------------------------------------------------------------------------------------------------------------##
# The Grandmaster dialogue
print(f"\nPleasure meeting ye, {player_name}.")
time.sleep(1)
skip_dialogue = input("Do you want to skip the Dialogue? (Yes/No): ").lower() == "yes"
if not skip_dialogue:
    print("Old Man: Now, prepare yourself to fight for the Land of Bravery to prove thyself!")
    time.sleep(2)
    print("\nThe old man then introduced you to the Grandmaster of the Guild, Lance")
    time.sleep(2)
    print(f"\nLance, the Grandmaster: 'Well well, Nice meeting you {player_name}.'")
    time.sleep(3)
    print(f"Lance, the Grandmaster: 'I wonder what made you think of stepping foot in our land... but I'll give you chance, you might have some uses...")
    time.sleep(2)
    print("Lance, the Grandmaster: 'Now if you're wanting to prove yourself trustworthy to me and my people,")
    time.sleep(2)
    print("Lance, the Grandmaster: 'You will have to help us fight for our land. You aren't able to do that without some equipments...'")
    time.sleep(2)
    print(f"\nLance, the Grandmaster: 'Now then, {player_name}...'")
    time.sleep(1)
else:
    print("You skipped the Dialogue!")
# Choosing of class
complete_quest(player_quests, "Welcome to the Land of Bravery!")
play_sound("quest completed", volume=0.6)
time.sleep(1.4)
add_quest(player_quests, "Forging a hero...", "Pick a class and a race.")
time.sleep(1.3)
print("\nChoose thy class: ")
time.sleep(1)
# Class list
print()
print("=======================================================================================================")
print("                                        -CLASS LIST-                                                   ")
print("=======================================================================================================")
print(f"(<{Fore.LIGHTGREEN_EX + Style.BRIGHT}Tip: Every class is unique, fun and balanced! Pick what you will enjoy and have fun!{Style.RESET_ALL}>)")
print()
# Warrior Description
print("1. Warrior – A hardened fighter with unmatched strength and resilience.")
print("[Base Health: 75 | Base Attack: 8]")
print("Special Skill: [Power Strike] - Unleash raw might to deliver a crushing blow that shatters defenses!")
# Rogue Description
print("\n2. Rogue – A swift shadow who strikes fast and critical.")
print("[Base Health: 50 | Base Attack: 9]")
print("Special Skill: [Shadow Step] - Vanish into darkness, striking swiftly and evading the next attack.")
# Mage Description
print("\n3. Mage – A frail but strong wielder of a devastating arcane power.")
print("[Base Health: 60 | Base Attack: 12]")
print("Special Skill: [Ice Shard] - Vanish into darkness, striking swiftly and evading the next attack.")
# Necromancer Description
print("\n4. Necromancer – A dark conjurer who commands the dead.")
print("[Base Health: 55 | Base Attack: 9]")
print("Special Skill: [Life Drain] - Sap the life (+3 Heal) from your enemy, wounding them as your own strength returns.")
print("Passive Skill: [Summon Undead] - Call upon forbidden rites to raise a fallen soul, binding it to your will to fight once more.")
# Marksman Description
print("\n5. Marksman – A precise hunter who slays from afar with deadly accuracy.")
print("[Base Health: 56 | Base Attack: 10]")
print("Special Skill: [Eagle Eye] - Focus with deadly precision — your next attack will have a guaranteed critical chance!")
# Paladin Description
print("\n6. Paladin – A holy knight who balances might with divine protection.")
print("[Base Health: 65 | Base Attack: 8]")
print("Special Skill: [Holy Shield] - Raise a divine barrier that blocks the next incoming strike.")
print("Passive Skill: [Holy Aura] - Call upon the Spirit and heal yourself for 3-5 HP upon defending")
# Druid Description
print("\n7. Druid – A nature sage who heals allies and bends the wilds.")
print("[Base Health: 60 | Base Attack: 11]")
print("Special Skill: [Regrowth] - Call upon nature’s essence (Heals 3-5 HP) to restore your vitality mid-battle.")
# Illusionist Description
print("\n8. Illusionist – A trickster who deceives foes and slips past danger.")
print("[Base Health: 57 | Base Attack: 10]")
print("Special Skill: [Mirror Image] - Create phantom doubles to confuse your foe to hit themselves and evade their blows.")
# Alchemist Description
print("\n9. Alchemist – A daring experimenter wielding volatile potions.")
print("[Base Health: 58 | Base Attack: 13]")
print("Special Skill: [Risky Play] - Gamble your safety for volatile power — throw your concoction & deal great damage or suffer the backlash.")
# Sentinel Description
print("\n10. Sentinel – A living bulwark, nearly unbreakable in defense.")
print("[Base Health: 80 | Base Attack: 7]")
print("Special Skill: [Bulwark Stance] - Fortify your body into living stone, reducing enemy damage but dulling your strikes.")
print("Passive Skill: [War Cry] - Cry for battle, increasing your attack!")
# Quit choiceeee
print("\nQ. Quit")
# Choice logic
choice = input("\nEnter 1-10 or 'q' to quit: ")
if choice.lower() == "q":
    print("Only such coward back off at the height of pressure, BE GONE!")
    sys.exit()
# Load the Class_stats
try:
    with open('class_data.json', 'r') as file:
        class_data = json.load(file)
except FileNotFoundError:
    print("Error: class_data.json is not found! Make sure the file is in the same folder as this script.")
# if player doesn't choose class welp villager you get!
villager_stats = {"name": "Villager", "health": 30, "attack": 5} # This is saying "if the player types a blank or anything else besides 1-10, they'll get a villager"
player_data = class_data.get(choice, villager_stats)
# Player data
player_class = player_data["name"]
max_health = player_data["health"]
player_health = player_data["health"]
attack_max = player_data["attack"]
# Dialogues for diff classes
if player_class == "Warrior":
    print("\nLance, the Grandmaster: 'Ah yes, the good ol' fashioned warrior. A strong, bruteforce of a might frontliner!'")
    time.sleep(2)
elif player_class == "Rogue":
    print("\nLance, the Grandmaster: 'Quite nimble I see? A rogue, a blade in the dark can be more decisive than a thousand swords.'")
    time.sleep(2)
elif player_class == "Mage":
    print("\nLance, the Grandmaster: 'Arcane huh? Thy power is not in the muscle, but in the mind.'")
    time.sleep(2)
elif player_class == "Necromancer":
     print("\nLance, the Grandmaster: 'Necromancy... a dangerous path, but necessary in these dark times. Just remember who's the master and who's the servant.'")
     time.sleep(2)
elif player_class == "Marksman":
    print("\nLance, the Grandmaster: 'Patience and a sharp aim eh? The true master of the hunt awaits their enemy's first mistake in the battle.'")
    time.sleep(2)
elif player_class == "Paladin":
    print("\nLance, the Grandmaster: 'Your faith is your shield, your purpose a guiding light, make sure to put those holy powers into good use.'")
    time.sleep(2)
elif player_class == "Druid":
    print("\nLance, the Grandmaster: 'Nature is on your side, I wonder what mother earth looks like?'")
    time.sleep(2)
elif player_class == "Illusionist":
    print("\nLance, the Grandmaster: 'A natural born deceiver are you eh? Tricking foes into thinking you're dead... but they were wrong...'")
    time.sleep(2)
elif player_class == "Alchemist":
    print("\nLance, the Grandmaster: 'A dangerous craft, but a rewarding one. You'll either find a solution or the answer you ere finding for.'")
    time.sleep(2)
elif player_class == "Sentinel":
    print("\nLance, the Grandmaster: 'Hard to take down, hard to kill. You'll be the shield to many, but also the saving force of your life.'")
    time.sleep(2)
elif player_class == "Dev test":
    race_name = "Dev"
    print("\nLance, the Grandmaster: 'Mmm, alright we got the dev in the house! Hi Dwayne! Good job so far keep it up!'")
    print("You want to test a specific chapter? (Y/N)")
    dev_choice = input("> ").strip().lower()
    if dev_choice == "y":
        print("What do you want to test?: ")
        time.sleep(1.5)
        print("[1] Chapter 1.  [2] Chapter 2.  [3] Chapter 3.")
        print("[4] Chapter 4.  [6] Chapter 6.")
        test = input("> ").strip()
        while True:
            if test == "1":
                pass
            elif test == "2":
                pass
            elif test == "3":
                chapt3_lost_trader()
                chapt4_the_last_bite()
            elif test == "4":
                chapt4_the_last_bite()
            elif test == "6":
                pass
    else:
        print("Okay go on")
else:
    print("\nLance, the Grandmaster: 'Oh, going with nothing huh? Such lowly and brave behaviour thy got, traveller.")
    time.sleep(2)
# PLayer Chooses race:
print(f"Lance, the Grandmaster: 'Wise choice {player_name}, Now If I may ask, what is thy race?'")
time.sleep(1)
print("Choose your Race:")
print()
print("=======================================================================================================")
print("                                           --RACE LIST--                                                   ")
print(f"\n(<{Fore.LIGHTGREEN_EX + Style.BRIGHT}Tip: Some races have discounts on certain shops, choose what you'll enjoy and have fun!{Style.RESET_ALL}>)")
print()
print("[1]. Human (+1 HP, +1 Atk.) - Balanced, Adaptable.")
print("[2]. Sylvari (-4 HP, +2 Atk.) - Agile Hunters, Favored by the forests.")
print("[3]. Gorvak (+12 HP, -1 Atk.) - Brutal strength, Ironblood endurance.")
print("[4]. Wraithkin (-8 HP, +4 Atk.) - Pale Wanderers.")
print("[5]. Solarian (+6 HP, +1  Atk.) - Sun-touched, Blessed with light.")
print("[6]. Stoneborn (+10 HP, +0 Atk.) - Stalwart children of the mountain.")
print("[7]. Kithling (-3 HP, +1 Atk.) - Smallfolk nimble in danger.")
print("[8]. Infernal (-6 HP, +2 Atk.) - Fire-blooded, feared by many.")
print("[9]. Drakonid (+11 HP, +2 Atk.) - Scions of Dragons, mighty and enduring.")
print("[10]. Lunari (-7 HP, +3 Atk.) - Moon-blessed people whose silver-tinged blood hums with ancient magic.")
print("=======================================================================================================")
print()
chosen_race = input("> ").strip()
# Player gets the race benefits

if chosen_race == "1":
    race_name = "Human"
    max_health += 1
    attack_max += 1
    print(f"Lance, the Grandmaster: 'Ah… it is decided. You carry the blood of the {race_name}, and you wield the mantle of the {player_class}.'")
    time.sleep(2)
    print(f"Lance, the Grandmaster: 'From this moment forth, {player_name}, you are a {race_name} {player_class} — sworn to the path of the Eternal Caverns.'")
    time.sleep(2)
elif chosen_race == "2":
    race_name = "Sylvari"
    max_health -= 4
    attack_max += 2
    print(f"Lance, the Grandmaster: 'Ah… it is decided. You carry the blood of the {race_name}, and you wield the mantle of the {player_class}.'")
    time.sleep(2)
    print(f"Lance, the Grandmaster: 'From this moment forth, {player_name}, you are a {race_name} {player_class} — sworn to the path of the Eternal Caverns.'")
    time.sleep(2)
elif chosen_race == "3":
    race_name = "Gorvak"
    max_health += 12
    attack_max -= 2
    print(f"Lance, the Grandmaster: 'Ah… it is decided. You carry the blood of the {race_name}, and you wield the mantle of the {player_class}.'")
    time.sleep(2)
    print(f"Lance, the Grandmaster: 'From this moment forth, {player_name}, you are a {race_name} {player_class} — sworn to the path of the Eternal Caverns.'")
    time.sleep(2)
elif chosen_race == "4":
    race_name = "Wraithkin"
    chosen_race = race_name
    max_health -= 8
    attack_max += 4
    print(f"Lance, the Grandmaster: 'Ah… it is decided. You carry the blood of the {race_name}, and you wield the mantle of the {player_class}.'")
    time.sleep(2)
    print(f"Lance, the Grandmaster: 'From this moment forth, {player_name}, you are a {race_name} {player_class} — sworn to the path of the Eternal Caverns.'")
    time.sleep(2)
elif chosen_race == "5":
    race_name = "Solarian"
    max_health += 6
    attack_max += 1
    print(f"Lance, the Grandmaster: 'Ah… it is decided. You carry the blood of the {race_name}, and you wield the mantle of the {player_class}.'")
    time.sleep(2)
    print(f"Lance, the Grandmaster: 'From this moment forth, {player_name}, you are a {race_name} {player_class} — sworn to the path of the Eternal Caverns.'")
    time.sleep(2)
elif chosen_race == "6":
    race_name = "Stoneborn"
    max_health += 10
    attack_max += 0
    print(f"Lance, the Grandmaster: 'Ah… it is decided. You carry the blood of the {race_name}, and you wield the mantle of the {player_class}.'")
    time.sleep(2)
    print(f"Lance, the Grandmaster: 'From this moment forth, {player_name}, you are a {race_name} {player_class} — sworn to the path of the Eternal Caverns.'")
    time.sleep(2)
elif chosen_race == "7":
    race_name = "Kithling"
    max_health -= 3
    attack_max += 1
    print(f"Lance, the Grandmaster: 'Ah… it is decided. You carry the blood of the {race_name}, and you wield the mantle of the {player_class}.'")
    time.sleep(2)
    print(f"Lance, the Grandmaster: 'From this moment forth, {player_name}, you are a {race_name} {player_class} — sworn to the path of the Eternal Caverns.'")
    time.sleep(2)
elif chosen_race == "8":
    race_name = "Infernal"
    max_health -= 6
    attack_max += 2
    print(f"Lance, the Grandmaster: 'Ah… it is decided. You carry the blood of the {race_name}, and you wield the mantle of the {player_class}.'")
    time.sleep(2)
    print(f"Lance, the Grandmaster: 'From this moment forth, {player_name}, you are a {race_name} {player_class} — sworn to the path of the Eternal Caverns.'")
    time.sleep(2)
elif chosen_race == "9":
    race_name = "Drakonid"
    max_health += 11
    attack_max += 2
    print(f"Lance, the Grandmaster: 'Ah… it is decided. You carry the blood of the {race_name}, and you wield the mantle of the {player_class}.'")
    time.sleep(2)
    print(f"Lance, the Grandmaster: 'From this moment forth, {player_name}, you are a {race_name} {player_class} — sworn to the path of the Eternal Caverns.'")
    time.sleep(2)
elif chosen_race == "10":
    race_name = "Lunari"
    max_health -= 7
    attack_max += 3
    print(f"Lance, the Grandmaster: 'Ah… it is decided. You carry the blood of the {race_name}, and you wield the mantle of the {player_class}.'")
    time.sleep(2)
    print(f"Lance, the Grandmaster: 'From this moment forth, {player_name}, you are a {race_name} {player_class} — sworn to the path of the Eternal Caverns.'")
    time.sleep(2)
else:
    print("You chose not to pick a race...")
    race_name = "Unknown"
player_health = max_health
time.sleep(1)
# Title welcoming the player
complete_quest(player_quests, "Forging a hero...")
time.sleep(1.3)
print(f"\n                                                            Welcome brave soul...        ")
print("                                                   === The Quest of the Eternal Caverns ===")
pygame.mixer.music.fadeout(2000)
time.sleep(1)
# Shop 1 narrative
pygame.mixer.music.load(r"sounds/shop1.ogg")
pygame.mixer.music.play(-1)
print("\nBefore your journey, you stopped by a small shop, 'Oak & Ember Mercantile'")
time.sleep(2)
door_open1 = pygame.mixer.Sound(r"sounds/open door.ogg")
door_open1.play()
print("Beyond the door lay a dim, crowded haven of relics — walls leaning inward, every inch crammed with clutter and secrets, the atmosphere dense enough to feel upon your skin...")
time.sleep(2)
print("But over the counter you see,")
time.sleep(1)
shop1_shopkeepers()
time.sleep(2)
beth_talks()
time.sleep(2)
# Shows the player the items
print(f"\n                           --[{player_name}, {race_name} {player_class} | {Fore.RED}{player_health}{Style.RESET_ALL}/{Fore.RED}{max_health}{Style.RESET_ALL} HP | {gold} {Fore.LIGHTYELLOW_EX}Gold{Style.RESET_ALL}]--")
print("===================================================================================================================================")
print(f"                                                      -SHOPKEEPER ITEMS-                                                               ")
print(f"    [1]. {Style.BRIGHT+ Fore.RED}Healing Potion{Style.RESET_ALL} (5 {Style.BRIGHT + Fore.YELLOW}gold{Style.RESET_ALL}) +10 HP healed")
print(f"    [2]. {Style.BRIGHT + Fore.WHITE}Silver Amulet{Style.RESET_ALL} (20 {Style.BRIGHT + Fore.YELLOW}gold{Style.RESET_ALL}) +5 attack")
print(f"    [3]. {Style.BRIGHT+ Fore.CYAN}Iron Shield{Style.RESET_ALL} (15 {Style.BRIGHT + Fore.YELLOW}gold{Style.RESET_ALL}) +10 Max HP")
print(f"    [Q]. {Style.BRIGHT}Show Quests.")
print(f"    [4]. {Style.BRIGHT}Leave Oak & Ember Mercantile.")
print("===================================================================================================================================")
#-----------------------------------------------------------------------------------------------------------#
# Shop 1 selection code
def shop_items():
    global gold, player_health, max_health, attack_max
    while True:
        buy = input("\nWhat would you like to buy? (1/2/3/4): ")
        if buy == "1":
            base_price = 5
            item_bought = "Healing Potion".lower()
            if race_name.lower() == "sylvari" and gold >= 5:
                discounted_price = 3
                print(f"Shopkeeper: Ah, a {race_name}! You might be in my favor... Only 3 gold for you.")
                time.sleep(1)
            else:
                discounted_price = base_price
            if gold >= discounted_price:
                player_payment()
                gold -= discounted_price
                potion_buy()
                time.sleep(1)
                potion_list[item_bought] = potion_list.get(item_bought, 0) + 1
                print(f"\nYou bought a Healing Potion! Now you have {potion_list[item_bought]} Potion(s) in your inventory. You now have {gold} gold coins.")
            else:
                shop1_broke()
        elif buy == "2" and gold >= 20:
            player_payment()
            attack_max += 5
            gold -= 20
            potion_buy()
            time.sleep(1)
            print(f"\nYou bought a Silver Amulet, your max ATTACK is now {attack_max}. + 5 attack. You now have {gold} gold coins.")
        elif buy == "3" and gold >= 15:
            player_payment()
            player_health += 10
            max_health += 10
            gold -= 15
            shield_buy()
            time.sleep(1)
            print(f"\nYou bought an Iron Shield,  your max HEALTH is now {max_health}. + 10 HP. You now have {gold} gold coins.")
        elif buy == "4":
            print("Shopkeeper: Best of luck in your journey, traveller.")
            pygame.mixer.music.fadeout(2000)
            break
        elif buy == "q":
            show_quest_log(player_quests)
        else:
            shop1_broke()
shop_items()

# noinspection PyUnusedLocal
def battle(enemy_key):
    global player_health, max_health, player_class, attack_max, player_inventory
    global gold
    global skill_cooldown, skill_cooldown_timer, regen_turns, regen_effect, attack_up_turns, attack_up_effect, damage_reduce_turns, defense_boost_turns, defense_boost_effect, invulnerable_turns, dodge_up_turns, dodge_up_effect
    global summoned, war_cry_turns, damage_multiplier, reduced_enemy_defense
    global reduced_enemy_attack, holy_shield_active, bulwark_active, bulwark_turns, bulwark_cd, enemy_confused,enemy_confused_turns
    ##
    while True:
        # Battle Loop
        run = False
        # reset all potion / turn-based buffs
        regen_turns = 0
        regen_effect = 0
        attack_up_turns = 0
        attack_up_effect = 0
        defense_boost_turns = 0
        defense_boost_effect = 0
        dodge_up_turns = 0
        dodge_up_effect = 0
        invulnerable_turns = 0
        # Get the enemy datas
        current_enemy = enemies[enemy_key].copy()
        enemy_health = current_enemy["health"]
        enemy_attack_stat = current_enemy["attack"]
        enemy_defence = current_enemy["defend_chance"]
        enemy_name = current_enemy["name"]
        poison_damage = current_enemy.get("poison", 0)
        poison_duration = current_enemy.get("poison_duration", 0)
        bleed_damage = current_enemy.get("bleed", 0)
        bleed_duration = current_enemy.get("bleed_duration", 0)
        venom_damage = current_enemy.get("venom", 0)
        venom_duration = current_enemy.get("venom_duration", 0)
        freeze_damage = current_enemy.get("freeze", 0)
        freeze_duration = current_enemy.get("freeze_duration", 0)
        # enemy battle condition
        while player_health > 0 and enemy_health > 0:
            defended = False
            dodging = False
            defended_by_spider = False
            # poison damage
            if poison_duration > 0 and poison_damage > 0:
                player_health -= poison_damage
                poison_duration -= 1
                print(f"The poison hurts you for {poison_damage} damage! (HP: {player_health}/{max_health})")
                time.sleep(1.5)
                if player_health <= 0:
                    print("You died from the poison... Strategize your attack next time...")
                    print("Do you want to restart the battle? (Yes/No): ")
                    restart = input("> ").lower().strip()
                    if restart == "yes":
                        player_health = max_health
                        enemy_health = current_enemy["health"]
                        continue
                    elif restart == "no":
                        print("Thanks for playing! Try it again and maybe experience the game in a different light!")
                        exit()
                    else:
                        print("Please type a valid option.")
            # Player bleeds
            if bleed_duration > 0 and bleed_damage > 0:
                player_health -= bleed_damage
                bleed_duration -= 1
                print(f"You are bleeding, you are being damaged for {bleed_damage}! (HP: {player_health}/{max_health})")
                time.sleep(1.5)
                if player_health <= 0:
                    print("You bled out... Strategize your defense next time...")
                    print("Do you want to restart the battle? (Yes/No): ")
                    restart = input("> ").lower().strip()
                    if restart == "yes":
                        player_health = max_health
                        enemy_health = current_enemy["health"]
                        continue
                    elif restart == "no":
                        print("Thanks for playing! Try it again and maybe experience the game in a different light!")
                        exit()
                    else:
                        print("Please type a valid option.")
            # Player frozen
            if freeze_duration > 0 and freeze_damage > 0:
                player_health -= freeze_damage
                freeze_duration -= 1
                print(f"The {enemy_name} inflicts a freezing effect on you! (HP: {player_health}/{max_health})")
                if player_health  <= 0:
                    print("You froze and died...")
                    print("Do you want to restart the battle? (Yes/No): ")
                    restart = input("> ").lower().strip()
                    if restart == "yes":
                        player_health = max_health
                        enemy_health = current_enemy["health"]
                        continue
                    elif restart == "no":
                        print("Thanks for playing! Try it again and maybe experience the game in a different light!")
                        exit()
                    else:
                        print("Please type a valid option.")
            # Player Is inflicted of venom
            if venom_duration > 0 and venom_damage > 0:
                player_health -= venom_damage
                venom_duration -= 1
                print(f"The {enemy_name} inflicts a venom on you! (HP: {player_health}/{max_health})")
                if player_health  <= 0:
                    print("You died of venom poisoning..")
                    print("Do you want to restart the battle? (Yes/No): ")
                    restart = input("> ").lower().strip()
                    if restart == "yes":
                        player_health = max_health
                        enemy_health = current_enemy["health"]
                        continue
                    elif restart == "no":
                        print("Thanks for playing! Try it again and maybe experience the game in a different light!")
                        exit()
                    else:
                        print("Please type a valid option.")

            # Battle starts this is or text showing
            print("--------------------------------------------------------------------------")
            print(f"             Your HP: {player_health}/{max_health} | {enemy_name} HP: {enemy_health}")
            print("--------------------------------------------------------------------------")
            print()
            if regen_turns > 0:
                player_health = min(max_health, player_health + regen_effect)
                regen_turns -= 1
                print(f"You regenerate {regen_effect} HP from a potion's lingering effect.")
                time.sleep(1.5)
            if attack_up_turns > 0:
                current_attack = attack_max + int(attack_max * attack_up_effect)
                attack_up_turns -= 1
                print("Your strength rises! Attack is increased by 15% for 3 turns.")
                time.sleep(1.3)
            else:
                current_attack = attack_max
            print("============================")
            print("       -BATTLE MENU-        ")
            print("============================")
            print()
            print()
            print(f"{Fore.RED}[1] Attack{Style.RESET_ALL}  {Fore.BLUE}[2] Defend{Style.RESET_ALL}")
            print(f"{Fore.GREEN}[3] Use Potion{Style.RESET_ALL}  {Fore.LIGHTYELLOW_EX}[4] Run{Style.RESET_ALL}")
            print(f"{Style.BRIGHT}[I] Inventory{Style.RESET_ALL}  {Fore.LIGHTBLUE_EX}[P] Potion List{Style.RESET_ALL}")
            print(f"    {Style.BRIGHT}[Q] Quest List{Style.RESET_ALL}")
            print()
            print("============================")
            print("     -SPECIAL ABILITIES-    ")
            print("============================")
            print()
            if player_class == "Sentinel":
                print(f"{Fore.BLUE}[W]. War Cry{Style.RESET_ALL}")
            if player_class == "Necromancer":
                print(f"{Fore.MAGENTA}[5]. Summon Undead{Style.RESET_ALL}")
            if skill_cooldown_timer == 0:
                print(f"{Fore.LIGHTGREEN_EX}[S]. Special Skill{Style.RESET_ALL}")
            print()
            action = input("> ").strip()  # the space for typing the choice
            #  Player actions
            # Player checks inventory or uses
            if action.lower() == "p":
                potion_lists()
                continue
            elif action.lower() == "i":
                open_inventory()
                continue
            elif action.lower() == "q":
                show_quest_log(player_quests)
                continue
             # Player attacks
            elif action == "1": # Attack codes
                damage = random.randint(1, attack_max)
                # enemy defense logic
                if random.random() < enemy_defence:
                    defended_by_spider = True
                    damage //= 2
                    print(f"The {enemy_name} defends against your attack!")
                grunt_sounds = current_enemy.get("grunt_sounds", []) # new learnings lol if i do [] it will make sure i dont get none incase no sounds
                if grunt_sounds:
                    grunt_file = random.choice(grunt_sounds)
                    grunt = pygame.mixer.Sound(grunt_file)
                    grunt.set_volume(0.7)
                    grunt.play()
                if damage_multiplier > 1:
                    damage *= damage_multiplier
                    damage_multiplier = 1
                    print("Eagle Eye lands a CRITICAL HIT!!!")
                    time.sleep(1.3)
                if war_cry_turns > 0:
                    damage += 3
                if defended_by_spider:
                    damage //= 2
                enemy_health -= damage
                print(f"You hit the {enemy_name} for {damage} damage!")
                time.sleep(1.5)
                # Necromancer summon bonus
                if summoned:
                    summon_damage = random.randint(2, 4)
                    enemy_health -= summon_damage
                    print(f"Your undead minion claws for {summon_damage} extra damage!")
                    time.sleep(1.3)

            elif action == "2":  # Defend code
                defending_sound = pygame.mixer.Sound(r"sounds/defended.ogg")
                defending_sound.set_volume(0.7)
                defending_sound.play()
                defended = True
                print(f"You defend against the {enemy_name}'s attack!")
                if player_class == "Paladin":
                    heal_amount = random.randint(3, 5)
                    player_health = min(max_health, player_health + heal_amount)
                    print(f"You defend the {enemy_name}'s attack and your holy aura heals {heal_amount} HP. ({player_health}/{max_health})")
                    time.sleep(1.3)
            elif action == "3": # Using potion code
                print("Which potion will you use?")
                print()
                print("================ <-POTIONS-> ==================")
                print()
                counter = 1
                available_potions = {}
                for potion_name, amount in potion_list.items():
                    if amount > 0 :
                        print(f"[{counter}]: {potion_name.title()} ({amount} left) ")
                        available_potions[str(counter)] = potion_name
                        counter += 1
                if not available_potions:
                    print("You don't have any potions to use!")
                    time.sleep(1.5)
                    continue
                print("=============================================")
                potion_choice = input("> ")
                if potion_choice in available_potions:
                    chosen_potion = available_potions[potion_choice]
                    potion_key = chosen_potion.lower()
                    if potion_key in potion_list:
                        potion_list[potion_key] -=1
                        heal_amount = potion_data.get(potion_key, 0)
                        player_inventory["empty bottle"] += 1
                        # Getting potion data
                        data = potion_data.get(potion_key, {})
                        heal = data.get("heal", 0)
                        effect = data.get("effect")
                        value = data.get("value")
                        duration = data.get("duration", 0)
                        player_health = min(max_health, player_health + heal)
                        print(f"You drink a {potion_key.title()} and restore {heal} HP. ({potion_list[potion_key]} left!)")
                        print(f"Empty bottles: {player_inventory['empty bottle']}.")
                        time.sleep(1.5)
                        # the potion effects
                        if effect == "regen_up":
                            regen_turns = duration
                            regen_effect = value
                            print(f"You feel a gentle warmth... HP will regenerate for {duration} turns.")
                            time.sleep(1.5)
                        elif effect == "attack_up":
                            attack_up_turns = duration
                            attack_up_effect = value
                            print(f"Your strength rises! Attack is up by 15% for {duration} turns.")
                        elif effect == "damage_reduce":
                            defense_boost_turns = duration
                            defense_boost_effect = value
                            print(f"A protective aura surrounds you, defense is increased for {duration} turns.")
                        elif effect == "cure":
                            poison_duration = 0
                            confused = 0
                            print("You are cured of all debuffs!")
                        elif effect == "dodge_up":
                            dodge_up_turns = duration
                            dodge_up_effect = value
                            print(f"You feel the wind rises as you move. Dodge chance increased for {duration} turns ")
                        elif effect == "invulnerable":
                            invulnerable_turns = duration
                            invulnerable_effect = value
                            print("The Lunar power showers over you... you are invulnerable for 1 turn.")
                            time.sleep(1.3)
                    else:
                        print("Invalid Choice.")
                else:
                    print("Invalid Choice.")

            elif action == "4":  # Run
                print("You fled the battle. The poisonous spider escapes...")
                print(f"You want to continue the game without fighting this enemy (Yes/No)? (-20 {Fore.LIGHTYELLOW_EX}gold{Style.RESET_ALL})")
                run_choice = input("\n> ").lower()
                if run_choice == "yes":
                    run = True
                    print("You fled the battle but ignored the enemy... dropping your gold...")
                    gold -= min(gold, gold -20)
                    print(f"Gold -20.")
                    break
                else:
                    print("Thanks for playing! Try again!")
                    exit()
            # Necromancer summoning undead minion
            elif action == "5" and player_class == "Necromancer":
                necro_summon = pygame.mixer.Sound(r"sounds/necromancer summon.ogg")
                necro_summon.set_volume(0.7)
                necro_summon.play()
                if not summoned:
                    summoned = True
                    print("You summon a fallen soul to fight by your side!")
                    time.sleep(1.3)
                    continue
                else:
                    print("You already have an undead minion!")
                    time.sleep(1.3)
            # Sentinel class using his War Cry
            elif action.lower() == "w" and player_class == "Sentinel":
                war_cry_turns = 3
                reduced_enemy_defense = 3
                print("You roar with a mighty War Cry! Your attack increases for 3 turns and the enemy’s defense weakens!")
                time.sleep(1.6)
                continue  # ends turn
            # Player using special skill
            elif action.lower() == "s" and skill_cooldown_timer == 0:
                print("\nYou unleash your SPECIAL SKILL!")
                skill_cooldown_timer = skill_cooldown
                # Warrior: Power Strike
                if player_class == "Warrior":
                    power_strike_sound = pygame.mixer.Sound(r"sounds/warrior power strike.ogg")
                    power_strike_sound.play()
                    damage = random.randint(10, 12)
                    enemy_health -= damage
                    print(f"You used POWER STRIKE, dealing {damage} damage!")
                    time.sleep(1.3)
                # Rogue: Shadow Step
                elif player_class == "Rogue":
                    dodge = pygame.mixer.Sound(r"sounds/dodging.ogg")
                    dodge.play()
                    damage = random.randint(6, 15)
                    enemy_health -= damage
                    dodging = True
                    print(f"You VANISH and strike for {damage} damage, preparing to dodge the next blow...")
                    time.sleep(1.3)
                # Mage: Ice Shard
                elif player_class == "Mage":
                    ice = pygame.mixer.Sound(r"sounds/ice shard.ogg")
                    ice.set_volume(0.7)
                    ice.play()
                    damage = random.randint(6, 13)
                    enemy_health -= damage
                    print(f"You used ICE SHARD therefore reducing the enemy's attack next turn and dealt {damage} damage!")
                    time.sleep(1.5)
                # Necromancer: Life Drain
                elif player_class == "Necromancer":
                    summoning = pygame.mixer.Sound(r"sounds/life drain.ogg")
                    summoning.set_volume(0.7)
                    summoning.play()
                    damage = random.randint(3, 6)
                    enemy_health -= damage
                    heal_amount = damage // 2
                    player_health = min(max_health, player_health + heal_amount)
                    print(f"Life Drain deals {damage} damage and heals you for {heal_amount} HP!")
                    time.sleep(1.3)
                # Marksman: Eagle Eye
                elif player_class == "Marksman":
                    eagle_eye_sound = pygame.mixer.Sound(r"sounds/eagle eye.ogg")
                    eagle_eye_sound.play()
                    damage_multiplier = 2
                    print("Eagle Eye activated! Next attack is guaranteed critical")
                    time.sleep(1.3)
                    continue
                # Paladin: Holy Shield
                elif player_class == "Paladin":
                    holy_shield_active = True
                    print("Holy Shield raised! Next enemy attack will be blocked!")
                    time.sleep(1.3)
                    continue
                # Druid: Regrowth
                elif player_class == "Druid":
                    druid_regrowth = pygame.mixer.Sound(r"sounds/druid heal.ogg")
                    druid_regrowth.set_volume(0.7)
                    druid_regrowth.play()
                    heal_amount = random.randint(6, 10)
                    player_health = min(max_health, player_health + heal_amount)
                    print(f"Regrowth heals you for {heal_amount} HP!")
                    time.sleep(1.3)
                    continue
                # Illusionist: Mirror Image
                elif player_class == "Illusionist":
                    mirror_image_sound = pygame.mixer.Sound(r"sounds/illusionist.ogg")
                    mirror_image_sound.play()
                    enemy_confused = True
                    dodging = True
                    damage = random.randint(4, 8)
                    enemy_health -= damage
                    enemy_confused_turns = 2
                    print(f"Mirror Image confuses the enemy and deals {damage} damage!")
                    time.sleep(1.3)
                # Alchemist: Risky Play
                elif player_class == "Alchemist":
                    risky_play_sound = pygame.mixer.Sound(r"sounds/risky play.ogg")
                    risky_play_sound.play()
                    if random.randint(1, 2) == 1:
                        damage = random.randint(8, 15)
                        enemy_health -= damage
                        print(f"Risky Play deals {damage} damage to the enemy!")
                        time.sleep(1.3)
                    else:
                        backfire = random.randint(3, 5)
                        player_health -= backfire
                        print(f"Risky Play backfires! You take {backfire} damage!")
                        time.sleep(1.3)
                # Sentinel: Bulwark Stance
                elif player_class == "Sentinel":
                    print("You used Bulwark Stance! Your defense grows for 50% but damage decreases by half!")
                    time.sleep(1.3)
                    bulwark_stance_sound = pygame.mixer.Sound(r"sounds/bulwark stance.ogg")
                    bulwark_stance_sound.play()
                    if bulwark_cd == 0:
                        bulwark_active = True
                        bulwark_turns = 2
                        bulwark_cd = 5

                # Dev test: Dev hammer lol
                elif player_class == "Dev test":
                    dev_hammer1 = pygame.mixer.Sound(r"sounds/Dev hammer1.ogg")
                    dev_hammer1.set_volume(1.0)
                    dev_hammer1.play()
                    time.sleep(3.5)
                    dev_hammer = pygame.mixer.Sound(r"sounds/Dev hammer.ogg")
                    dev_hammer.set_volume(1.0)
                    dev_hammer.play()
                    damage = random.randint(20, 100)
                    enemy_health -= damage
                    time.sleep(1.5)
                    print(f"You used Dev hammer! Ban him! You hit the enemy for {damage}")
                    time.sleep(1.3)
            else:
                print("You hesitated and lose your turn!")
                time.sleep(1.3)
            # Enemy enrages
            if enemy_name == "Vermillion Tyrant" and enemy_health <= 30 and not current_enemy.get("rage", False):
                current_enemy["rage"] = True
                enemy_attack_stat += 5
                print(f"{enemy_name} roars with unholy fury! Its damage is increased significantly!")
                time.sleep(1.3)
            #  enemy Attack
            if enemy_health > 0:
                enemy_damage = random.randint(1, enemy_attack_stat)
                # enemy confused by illusionist
                if enemy_confused:
                    print(f"{enemy_name} looks disoriented and hits themselves in confusion!")
                    time.sleep(1.3)
                    confuse_damage = random.randint(1,3)
                    enemy_health -= confuse_damage
                    enemy_confused_turns -= 1
                    if enemy_confused_turns <= 0:
                        enemy_confused = False
                        print(f"{enemy_name} shakes off the confusion!")
                        time.sleep(1.3)
                        continue
                # Player gets invulnerability
                if invulnerable_turns > 0:
                    print("You are invulnerable! No damage taken.")
                    time.sleep(1.3)
                    enemy_damage = 0
                    invulnerable_turns -= 1
                # Player puts reduced damage debuff on enemy
                if reduced_enemy_attack:
                    enemy_attack_stat -= reduced_enemy_attack
                    reduced_enemy_attack = 0
                    print("The enemy's damage is now reduced for the next turn!")
                    time.sleep(1.3)
                # Player's defense boost
                if defense_boost_turns > 0:
                    enemy_damage = int(enemy_damage * (1 - defense_boost_effect))
                    defense_boost_turns -= 1
                    print("You feel your skin harden against the attacks!")
                    time.sleep(1.3)
                # Player with some potions have a 10% chance of dodge
                if dodge_up_turns > 0:
                    if random.random() < dodge_up_effect:
                        dodging = True
                    dodge_up_turns -= 1
                # Player dodges or is invulnerable
                if dodging:
                    print(f"You completely dodge the {enemy_name}'s attack!")
                    enemy_damage = 0
                    dodging = False
                    time.sleep(1.3)
                # Player defends against enemy damage
                if defended:
                    enemy_damage //= 2
                # Holy Shield turns on and off
                if holy_shield_active:
                    paladin_shield = pygame.mixer.Sound(r"sounds/paladin shield.ogg")
                    paladin_shield.set_volume(0.7)
                    paladin_shield.play()
                    print(f"Holy Shield blocks the {enemy_name}'s attack!")
                    enemy_damage = 0
                    holy_shield_active = False
                    time.sleep(1.3)
                # Bulwark debuff on enemy
                if bulwark_active:
                    enemy_attack_stat //= 2
                # Bulwark turns on and off
                if player_class == "Sentinel":
                    if bulwark_turns:
                        bulwark_turns -= 1
                        if bulwark_turns == 0:
                            bulwark_active = False
                            print("Your Bulwark Stance wears off...")
                            time.sleep(1.3)
                # Enemy damaging the player
                player_health -= enemy_damage
                player_hit = pygame.mixer.Sound(r"sounds/player hit.ogg")
                player_hit.play()
                print(f"The {enemy_name} hits you for {enemy_damage} damage!")
                time.sleep(1.3)
                # Player's chances of getting poisoned  and it's duration
                if poison_damage > 0 and poison_duration == 0 and random.randint(1, 4) == 1:
                    poison_duration = 2
                    print(f"\nThe {enemy_name} poisons you!")
                    time.sleep(1.3)
                # Player's chance of bleeding
                if bleed_damage > 0 and bleed_duration == 0 and random.randint(1, 5) == 1:
                    bleed_duration = 3
                    print("\nYour blood drips...")
                    time.sleep(1.3)
                # Player's chance of freezing
                if freeze_damage > 0 and freeze_duration == 0 and random.randint(1, 4) == 1:
                    freeze_duration = 2
                    print("You are freezing...")
                    time.sleep(1.3)
                # Player's chance of getting venomed
                if venom_damage > 0 and venom_duration > 0 and random.randint(1, 5) == 1:
                    venom_duration = 3
                    print(f"The {enemy_name} inflicted you with venom!")
                    time.sleep(1.3)
            # Turn Ends
            if player_class == "Sentinel":
                if war_cry_turns > 0:
                    war_cry_turns -= 1
            if skill_cooldown_timer > 0:
                skill_cooldown_timer -= 1
                if skill_cooldown_timer == 0:
                    print("Your SPECIAL SKILL is ready!")
                    time.sleep(1)
        # Poisonous spider defeated or player defeated
        if player_health <= 0:
            print(f"\nYou died... The {enemy_name} triumphs over you.")
            print("Do you want to restart the battle? (Yes/No): ")
            restart = input("> ").lower().strip()
            if restart == "yes":
                player_health = max_health
                enemy_health = current_enemy["health"]
                continue
            elif restart == "no":
                print("Thanks for playing! Try it again and maybe experience the game in a different light!")
                exit()
            else:
                print("Please type a valid option.")
        else:
            if run:
                print("You ran away, you didn't get any gold...")
                break
            else:
                victory = pygame.mixer.Sound(r"sounds/victory.ogg")
                victory.play()
                min_gold, max_gold = sorted(current_enemy["gold_loot"])
                gold_earned = random.randint(min_gold, max_gold)
                gold += gold_earned
                print(f"\nYou killed the {enemy_name} and looted {gold_earned} gold! (Gold: {gold})")
                time.sleep(1.3)
                item_loot = current_enemy.get("item_loot", [])
                if item_loot and random.random() < 0.5:
                    dropped_items = random.choice(item_loot)
                    player_inventory[dropped_items] = player_inventory.get(dropped_items, 0) + 1
                    print(f"The {enemy_name} dropped a {dropped_items}")
                break
# Before going to the caverns narrative
pygame.mixer.music.load(land_of_bravery_bgm)
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)
# CHapter 2
add_quest(player_quests, "First big step!", "Head down to the Eternal Caverns and conquer what's coming...")
chapt2_eternal_caverns()
# Goblin fight narration
pygame.mixer.music.fadeout(2000)
print("\nA goblin jumps out from the shadows!\nThe battle begins!\n")
time.sleep(1)
# Goblin battle music
pygame.mixer.music.load(r"sounds/battle music.ogg")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)
# Battle loop goblin
battle("Goblin")
# Lost trader encounter narration
pygame.mixer.music.load(r"sounds/hidden passage.ogg")
pygame.mixer.music.set_volume(0.9)
pygame.mixer.music.play(-1)
complete_quest(player_quests, "First big step!")
chapt3_lost_trader()
# Chapter 4 Music
pygame.mixer.music.load(r"sounds/chapter 4.ogg")
pygame.mixer.music.play(-1)
chapt4_the_last_bite()
# Chapter 5: The Eternal village
pygame.mixer.music.load(r"sounds/Eternal Village bg.ogg")
pygame.mixer.music.play(-1)
# -Chapter 5-
def chapt5_eternal_village():
    global gold, hearthfire_stock, mead_stock, player_health, spirits_stock, max_health, attack_max, player_class, player_name
    print("\nChapter 5: The Eternal Village...")
    time.sleep(1)
    print(
        "The Eternal Village: It is more than streets and shops; it is a labyrinth carved from the caverns themselves."
        "\nNarrow alleys twist like veins between ancient buildings."
        "\nLanterns sway in the cavern drafts, throwing dancing light upon runes etched long ago."
        "\nThe Hollow Earth Inn and weapon shop stand as familiar anchors, yet every hidden corner and shadow promises secrets that have endured through centuries underground,"
        " waiting for the eyes of the curious."
        "\nDragon Trainers and Eternal Mages left and right are seen."
    )
    print(f"\n                           --[{player_name}, {race_name} {player_class} | {Fore.RED}{player_health}{Style.RESET_ALL}/{Fore.RED}{max_health}{Style.RESET_ALL} HP | {gold} {Fore.LIGHTYELLOW_EX}Gold{Style.RESET_ALL}]--")
    skip_dialogue1 = input("\nWould you like to skip the dialogue? (Yes/No)\n> ").lower() == "yes"
    if not skip_dialogue1:
        time.sleep(2)
        print("\nAfter you talked with the Eternal warrior, The Eternal villagers praised you!"
              " You looked around and you see many shops and houses, built with Spruce, stone and Crystals..")
        time.sleep(3)
        print(
            "Before thee lies the Eternal Village, its cobblestones smoothed by countless generations. To thy right, the Hollow Earth Inn glows with golden hearthfire, smoke curling like ancient whispers into the sky.")
        time.sleep(4)
        print(
            "On thy left, a shop stands firm, its wooden beams etched with runes and scars from years of craftsmanship.")
        time.sleep(2)
        print(
            "All about thee, narrow alleys twist like the roots of a great tree, lanterns swaying in the gentle wind, and the air hums with secrets of centuries past. "
            "Every shadow and stone seems to hold a story, waiting for those bold enough to seek it.")
        time.sleep(4)
        south_eternal_village()
    else:
        print("You skipped the Dialogue!")
        pygame.mixer.music.fadeout(2000)
        south_eternal_village()

    # Start of the Chapter 5 Eternal village adventure
def south_eternal_village():
    global player_name, player_class, race_name, player_health, max_health, attack_max, gold, player_inventory
    global hearthfire_stock, mead_stock, spirits_stock, hp_change
    while True:
        pygame.mixer.music.load(r"sounds/Eternal Village bg.ogg")
        pygame.mixer.music.play(-1)
        print()
        print(f"\n                        --[{player_name}, {race_name} {player_class} | {Fore.RED}{player_health}{Style.RESET_ALL}/{Fore.RED}{max_health}{Style.RESET_ALL} HP | {gold} {Fore.LIGHTYELLOW_EX}Gold{Style.RESET_ALL}]--")
        move = input("Where do you want to go?"
                     "\n[1]. East. - The Hollow Earth Tavern"
                     "\n[2]. West - Stoneheart Armory"
                     "\n[3]. North - Hall of the Everlight,The Spindle of Tales, and more..."
                     "\n[4]. Talk to the Eternal Warrior."
                     "\n> ").strip()
        # Player goes to the Tavern
        if move == "1":
            print("You walk to the East and saw a Tavern and you see its name, 'The Hollow Earth Tavern'.")
            time.sleep(2)
            door_open = pygame.mixer.Sound(r"sounds/open door.ogg")
            door_open.play()
            print("Amber light flickers over damp stone as you step inside, "
                  "and you see many Eternal Villagers eating, talking together, some dancing.")
            time.sleep(2)
            print("Warm hearth-heat pushes back the cavern's chill. "
                  "The air smells of spiced meat, sweet herb-like aroma of the foods...")
            pygame.mixer.music.fadeout(2000)
            time.sleep(4)
            # Player choice in tavern
            pygame.mixer.music.load(r"sounds/Tavern.ogg")
            pygame.mixer.music.play(-1)
            while True:
                print(f"\n                                          --[{player_name}, {race_name} {player_class} | {Fore.RED}{player_health}{Style.RESET_ALL}/{Fore.RED}{max_health}{Style.RESET_ALL} HP | {gold} {Fore.LIGHTYELLOW_EX}Gold{Style.RESET_ALL}]--")
                walk_choice = input(
                    "\nWhat do you want to do?\n"
                    "[1]. Talk to the bartender\n"
                    "[2]. Ask an Eternal Being about this Eternal Village\n"
                    "[3]. Leave the Hollow Earth Inn.\n> ")
                # Player speaks to bartender
                if walk_choice == "1":
                    print("You walk towards the Bartender.")
                    speak_eternal_bartender()
                    time.sleep(3)
                    print(f"You have {gold} gold.")
                    # Menu of the Tavern
                    while True:
                        print(f"\n                     --[{player_name}, {race_name} {player_class} | {Fore.RED}{player_health}{Style.RESET_ALL}/{Fore.RED}{max_health}{Style.RESET_ALL} HP | {gold} {Fore.LIGHTYELLOW_EX}Gold{Style.RESET_ALL}]--")
                        buy_choice = input(
                            "You look at the menu:\n"
                            f"[1]. Hearthfire Ale (10 gold, {hearthfire_stock} stock left ) - A warm, spiced ale brewed from cavern grains and glowcap mushrooms.\n"
                            f"[2]. Amber Mead (10 gold, {mead_stock} stock left) - Sweet honey mead served in a heavy stone mug.\n"
                            f"[3]. Spirits of the Depths (15 gold, {spirits_stock} stock left) - A strong, clear liquor distilled from cavern roots.\n"
                            f"[4]. 'Bye'\n> ")
                        # Player buys Hearthfire Ale
                        if buy_choice == "1":
                            if hearthfire_stock > 0 and gold >= 10:
                                hearthfire_stock -= 1
                                gold -= 10
                                attack_max += 10
                                print(f"{player_name}: 10 gold for the Hearthfire, if it please thee.'")
                                time.sleep(2)
                                print("Eternal Bartender: 'Ah, yes, the town's favorite. This ale "
                                      "has said to increase the will of the person drinkin.'")
                                time.sleep(3)
                                print("The Eternal Bartender pours the Hearthfire Ale into a mug...")
                                time.sleep(1)
                                print(f"You drink the Hearthfire Ale, increasing your max attack! "
                                      f"Max attack is now {attack_max} +10.")
                                print(f"You now have {gold} gold left.")
                                time.sleep(2)
                            else:
                                no_gold_tavern()
                        # Player buys Amber mead
                        elif buy_choice == "2":
                            if mead_stock > 0 and gold >= 10:
                                mead_stock -= 1
                                gold -= 10
                                max_health += 30
                                print(f"{player_name}: 'Pour me the mead that flows like golden honey.'")
                                time.sleep(2)
                                print("Eternal Bartender: 'To you the pleasure, traveller.'")
                                time.sleep(1)
                                print("The Eternal Bartender pours the aromatic mead into a mug...")
                                time.sleep(1)
                                print(
                                    f"You drink the Amber Mead, increasing your max HP. Your max HP is now {max_health} +30.")
                                time.sleep(2)
                            else:
                                no_gold_tavern()
                        # Player Buys Spirits of the Depths
                        elif buy_choice == "3":
                            if spirits_stock > 0 and gold >= 15:
                                spirits_stock -= 1
                                gold -= 15
                                hp_change = 10
                                print(f"{player_name}: 'Grant me a draught of Spirits of the Depths, good barkeep.'")
                                time.sleep(1.5)
                                print(
                                    "Eternal Bartender: 'Ah… bold choice, traveler. ‘Spirits of the Depths,’ brewed from cavern herbs and whispers of old… handle with care, lest it stir more than your courage tonight.'")
                                time.sleep(2.3)
                                if random.randint(0, 1) == 0:
                                    player_health -= hp_change
                                    if player_health < 0:
                                        player_health = 0
                                    print(f"Your health collapses from the power of the spirits -{hp_change}. "
                                          f"Your health is now {player_health}/{max_health}.")
                                    time.sleep(2)
                                else:
                                    player_health += hp_change
                                    if player_health > max_health:
                                        player_health = max_health
                                    print(f"The Spirits invigorate you +{hp_change}! Your health is now {player_health}/{max_health}.")
                                    time.sleep(2)
                            else:
                                no_gold_tavern()
                        elif buy_choice == "4":
                            print("See you around, traveller.")
                            break
                        else:
                            print("Please enter a valid option.")
                # Player given the choice to do somethings inside the tavern
                elif walk_choice == "2":
                    print(f"\n                              --[{player_name}, {race_name} {player_class} | {Fore.RED}{player_health}{Style.RESET_ALL}/{Fore.RED}{max_health}{Style.RESET_ALL} HP | {gold} {Fore.LIGHTYELLOW_EX}Gold{Style.RESET_ALL}]--")
                    while True:
                        ask = input(f"{player_name} (What do you want to say, traveller?): \n"
                                    "[1]. 'Greetings, If I may ask, what is the history if this village?'\n"
                                    "[2]. 'Have you heard of an Old Man, with bald hair, white beard, around here?'\n"
                                    "[3]. 'Well met.'\n> ")
                        if ask.strip().lower() == "1":
                            eternal_village()
                            time.sleep(3)
                        elif ask.strip().lower() == "2":
                            eternal_villager_ask()
                            time.sleep(3)
                        elif ask.strip().lower() == "3":
                            eternal_villager_bye()
                            time.sleep(3)
                            break
                        else:
                            print("Please enter a valid option.")
                # Player chooses 3 to leave the inn
                elif walk_choice == "3":
                    pygame.mixer.music.fadeout(2000)
                    door_close2 = pygame.mixer.Sound(r"sounds/close door.ogg")
                    door_close2.play()
                    print(
                        "You step out of the Hollow Earth Inn, the smell of roasted meat and smoke fading behind you as the village square spreads ahead...")
                    time.sleep(2)
                    break
                else:
                    print("Please enter a valid option.")
        # Player goes to West
        elif move == "2":
            print("Heading west, the cobblestones give way to narrower alleys. The scent of burning wood mixes with the chatter of villagers...")
            time.sleep(1)
            print("\nYou tread deeper into the cavern street, the echo of your steps swallowed by stone."
                  " Ahead, a faint red glow flickers against the walls — the forge of the Stoneheart Armory, carved straight into the rock itself."
                  " Its heavy doors bear scars of countless strikes, as though the cavern remembers every weapon born within.")
            time.sleep(3)
            print("You enter the Stoneheart Armory, The scent of coal and hot iron hangs heavy; rows of blades glimmer like watchful eyes in the cavern light")
            time.sleep(3)
            shop2_armorer()
            time.sleep(2)
            # Shop 2 (Stoneheart Armory) choice
            stoneheart_armory_shop()
            south_eternal_village()
        # Player chooses to go North (3. North)
        elif move == "3":
            print(
                "You head North, where the towering Hall of the Everlight glows like a beacon, the Spindle of Tales hums with forgotten stories,"
                " and the Echoing Vilas Apothecary breathes a scent of strange potions through the cool cavern air.")
            time.sleep(2)
            print(f"\n                                  --[{player_name}, {race_name} {player_class} | {Fore.RED}{player_health}{Style.RESET_ALL}/{Fore.RED}{max_health}{Style.RESET_ALL} HP | {gold} {Fore.LIGHTYELLOW_EX}Gold{Style.RESET_ALL}]--")
            time.sleep(1)
            print("Where do you want to go?"
                  "\n[1]. Walk to the Spindle of Tales."
                  "\n[2]. Venture through the Hall of the Everlight. (Coming soon)"
                  "\n[3]. Go to the Echoing Vials (Potions Shop)."
                  "\n[4]. Explore deeper in the Eternal Caverns. (Coming soon)"
                  "\n[5]. Check out the Glowmire Market. (Coming soon)"
                  "\n[6]. Visit the Eternal Sanctuary."
                  "\n[7]. Compete in the Rift of Echoing Souls."  
                  "\n[S]. Go back.")
            walk_choice_north = input("> ")
            # Player chooses where to go
            if walk_choice_north == "1":
                print("You step inside, and the air smells of parchment and candle smoke. "
                      "Threads of light twist through the room, weaving stories you have yet to hear.")
                time.sleep(2)
                print("As you're inside, you see an inscription on the wall,")
                time.sleep(1)
                print("Where sunlight fades and echoes keep,")
                time.sleep(1)
                print("A burning leaf in shadows deep.")
                time.sleep(1)
                print("Follow whispers, stone and stream,")
                time.sleep(1)
                print("There lies the blossom of ember’s gleam.")
                time.sleep(2)
                loreweaver_greet_lines()
                time.sleep(2)
                while True:
                    print(f"\n                                --[{player_name}, {race_name} {player_class} | {Fore.RED}{player_health}{Style.RESET_ALL}/{Fore.RED}{max_health}{Style.RESET_ALL} HP | {gold} {Fore.LIGHTYELLOW_EX}Gold{Style.RESET_ALL}]--")
                    print("What do you want to do?"
                          "\n[1]. Speak to the Loreweaver about the Enchanted Scroll."
                          "\n[2]. Browse shelves of Books & Scrolls."
                          "\n[3]. Spin the Threads of Fate."
                          "\n[4]. Leave the Spindle of Tales.")
                    player_choice_2 = input("> ")
                    # Player chooses 1st option, to talk with the Loreweaver
                    if player_choice_2 == "1":
                        loreweaver_quest_lines()
                        time.sleep(2)
                        print("Do you want to accept this quest? (Yes/No)")
                        while True:
                            quest_accept = input(">> ").strip().lower()
                            if quest_accept == "yes":
                                add_quest(player_quests, "The answers lies in the scroll.", "Find an Emberleaf Blossom deeper onto the cave...")
                                time.sleep(1.3)
                            elif quest_accept == "no":
                                print("You stepped away from the Loreweaver...")
                                break
                            else:
                                print("Invalid choice, Traveller.")
                    # Player chooses to browse and read the glowing book in the shelves
                    elif player_choice_2 == "2":
                        print("You wandered around the abode, and a certain glowing book caught your eye and whispered to yourself,")
                        time.sleep(2)
                        print(f"{player_name}: 'Mmm? Interesting...'")
                        time.sleep(1.5)
                        print("As you read the book a certain line spoke to you,")
                        time.sleep(1.4)
                        print("\n'...beware the elder who opens the path, for his steps echo deeper than yours.'")
                        time.sleep(2)
                        print("You whispered to yourself again,")
                        time.sleep(1.5)
                        print(f"\n{player_name}: elder... what could this mean?")
                        time.sleep(2)
                        print(
                            "\nYou close the book and put it back at the shelf, leaving yourself questioning what it meant...")
                        time.sleep(2)
                    # Player chooses to spin the Threads of Fate
                    elif player_choice_2 == "3":
                        print(f"You slowly stepped closer to the Threads of Fate as it was whispering your name,")
                        time.sleep(2)
                        print(f"{player_name}, {player_name}... come closer and know thy fate...")
                        time.sleep(2)
                        print("You spun the Thread of Fate...")
                        time.sleep(1.4)
                        thread_of_fate()
                        time.sleep(2)
                    # Player leaves Spindle of Tales
                    elif player_choice_2 == "4":
                        loreweaver_farewell_lines()
                        time.sleep(2)
                        print(
                            "You step out of the Spindle of Tales, and the familiar streets of the Eternal Cavern Village stretch before you,"
                            " bathed in the soft glow of lanterns that dance like distant stars.")
                        time.sleep(2)
                        break
            elif walk_choice_north == "2":
                print("Coming soon... Chapter 6: Truth unveiled")
                time.sleep(1.3)
                print("Thanks for giving my game a chance, You can still try the other features.")
            elif walk_choice_north == "3":
                print("You head towards Echoing Vials, where the faint clink of glass and low hum of bubbling concoctions drift through the stone corridors.")
                time.sleep(2)
                echo_binder_greetings_lines()
                pygame.mixer.music.fadeout(2000)
                time.sleep(2)
                pygame.mixer.music.load(r"sounds/echoing vials.ogg")
                pygame.mixer.music.play(-1)
                while True:
                    print(f"\n                          --[{player_name}, {race_name} {player_class} | {Fore.RED}{player_health}{Style.RESET_ALL}/{Fore.RED}{max_health}{Style.RESET_ALL} HP | {gold} {Fore.LIGHTYELLOW_EX}Gold{Style.RESET_ALL}]--")
                    print("What do you want to do?")
                    time.sleep(1)
                    time.sleep(1.5)
                    print("\n--> [1]. Buy Potions & Vials."
                          "\n--> [2]. Donate to the Eternal Villagers Community."
                          "\n--> [3]. Trade items."
                          "\n--> [4]. Check Inventory"
                          "\n--> [X]. Leave the Echoing Vials.")
                    player_choice_1 = input("> ")
                    if player_choice_1 == "1":
                        print("You went closer to the Echo Binding desk...")
                        time.sleep(1.5)
                        echo_binder_menu_lines()
                        time.sleep(1.7)
                        shop_choice()
                    elif player_choice_1 == "2":
                        print("You walk towards the donation area...")
                        time.sleep(1.5)
                        print("A faintly glowing bowl rests upon the table, humming with unseen energy.")
                        time.sleep(1.3)
                        echo_vials_donation()
                    # Player trades with the NPC
                    elif player_choice_1 == "3":
                        print("You walked towards the trading station...")
                        time.sleep(1.3)
                        print("Eternal Trader: 'Greetings traveller, what might have ye for me?'")
                        time.sleep(1.7)
                        player_inventory, gold = echo_vials_trade(player_inventory, gold)
                    # Player opens the inventory
                    elif player_choice_1 == "4":
                        print("You open your Inventory...")
                        time.sleep(1.3)
                        open_inventory()
                    elif player_choice_1 == "x":
                        print("You walk out of the Echoing Vials, the bubbling of the potions are heard fainting behind you...")
                        pygame.mixer.music.fadeout(2000)
                        break
            elif walk_choice_north == "4":
                print("Coming soon! You can try Rift of Echoing Souls to test your skills and test out diff classes!")
                time.sleep(1.3)
            elif walk_choice_north == "5":
                print("Coming soon! You can try Rift of Echoing Souls to test your skills and test out diff classes!")
            elif walk_choice_north == "6":
                print("You approach the Eternal Sanctuary, its glow calm yet heavy, as if the walls remember every soul...")
                time.sleep(1.5)
                door_opening_sound()
                print("You step into the Eternal Sanctuary. Candlelight dances across wooden beams, the scent of herbs and stew wrapping around you like a quiet welcome.")
                time.sleep(2)
                eternal_inkeeper_greeting()
                time.sleep(1.7)
                print("What do you want to do?")
                time.sleep(0.3)
                while True:
                    print("]================================[ ETERNAL SANCTUARY ]====================================[")
                    print(f"                                 -[{player_name} | {Fore.RED}{player_health}{Style.RESET_ALL}/{Fore.RED}{max_health}{Style.RESET_ALL} | {gold} {Fore.LIGHTYELLOW_EX}Gold{Style.RESET_ALL}]-")
                    print(f"[1]. Rent a room to rest (restore full health) (Price: 50 {Fore.LIGHTYELLOW_EX}Gold{Style.RESET_ALL})  [2]. Order Food/Drink")
                    print(f"[3]. Play 'Fortune's Toss'.  [4]. Talk to the Eternal Inkeeper.")
                    print(f"[X]. Leave Eternal Sanctuary.")
                    print("]=========================================================================================[")
                    player_choice_3 = input("--> ").strip().lower()
                    if player_choice_3 == "1":
                        print(f"{player_name}: 'A room for the night, if it please thee.'")
                        time.sleep(1.3)
                        if gold >= 50:
                            gold -= 50
                            soulwarden_greetings_lines()
                            time.sleep(1.5)
                            print("The Soulwarden: Now would thy sign your name on this paper.")
                            time.sleep(1.4)
                            print("You wrote your name and signed the rental papers and handed over your payment...")
                            time.sleep(1.6)
                            print("You rented a room to stay the night...")
                            time.sleep(1.3)
                            player_sleeping()
                            time.sleep(2)
                            player_health = max_health
                            print(f"You rested well, your health got restored to its full HP. [{player_health}/{max_health} HP].")
                        else:
                            print("The Soulwarden: Thy hast no more Gold, adventurer. Come back again when thy have enough.")
                    elif player_choice_3 == "2":
                        print("You walked towards the tasty and soothing smell of the food...")
                        time.sleep(1.3)
                        serah_line()
                        time.sleep(1.3)
                        while True:
                            print("What do you want from the menu?")
                            print("=" * 60)
                            print("                                                                        --|- SANCTUARY FOOD MENU -|--")
                            print("=" * 60)
                            print(f"                                    -[{player_name} | {Fore.RED}{player_health}{Style.RESET_ALL}/{Fore.RED}{max_health}{Style.RESET_ALL} | {gold} {Fore.LIGHTYELLOW_EX}Gold{Style.RESET_ALL}]-")
                            print(f"[1]. {Fore.YELLOW + Style.BRIGHT}Celestial Broth{Style.RESET_ALL} 15 {Fore.LIGHTYELLOW_EX}Gold{Style.RESET_ALL} (+10 HP) - A soothing golden soup for weary souls"
                                  f"\n[2]. {Fore.GREEN + Style.BRIGHT}Embergrain Stew{Style.RESET_ALL} 20 {Fore.LIGHTYELLOW_EX}Gold{Style.RESET_ALL} (+5 HP & +2 ATK) - Hearty grains and roots simmered slow."
                                  f"\n[3]. {Fore.LIGHTMAGENTA_EX + Style.BRIGHT}Moonpetal Salad{Style.RESET_ALL} 30 {Fore.LIGHTYELLOW_EX}Gold{Style.RESET_ALL} (+15 HP) - Crisp greens with shimmering petals."
                                  f"\n[4]. {Fore.CYAN + Style.BRIGHT}Sunforged Bread{Style.RESET_ALL} 25 {Fore.LIGHTYELLOW_EX}Gold{Style.RESET_ALL} (+8 HP, +3 ATK) - Warm bread baked with eternal embers."
                                  f"\n[5]. {Fore.LIGHTRED_EX + Style.BRIGHT}Eternal Roast{Style.RESET_ALL} 40 {Fore.LIGHTYELLOW_EX}Gold{Style.RESET_ALL}, {eternal_roast_stock} Stock left (+20 HP +5 ATK) - Tender meat infused with sacred herbs."
                                  f"\n[X]. {Style.BRIGHT}Exit Menu{Style.RESET_ALL}")
                            print("=" * 60)
                            sanctuary_resto_choice = input("\n--> ").lower().strip()
                            while True:
                                # Player chooses "1" and buys Celestial broth
                                if sanctuary_resto_choice == "1" and gold >= 15:
                                    if race_name == "Kithling" and gold >= 12:
                                        print("Serah the Sustenance: Ahh yes a Kithling! I favor thee!")
                                        time.sleep(1.3)
                                        print(f"You bought Celestial Broth with a discounted price of 3 Gold! -12 Gold, gold is now {gold} Gold. Max HP is now {max_health}.")
                                        player_payment()
                                        time.sleep(1.3)
                                        gold -= 12
                                        max_health += 10
                                        break
                                    else:
                                        gold -= 15
                                        max_health += 10
                                        print(f"You bought Celestial Broth! -15 Gold, gold is now {gold} Gold. Max HP is now {max_health}")
                                        player_payment()
                                        time.sleep(1.3)
                                        break
                                # Player chooses "2" and buys Embergrin Stew
                                elif sanctuary_resto_choice == "2" and gold >= 20:
                                    if race_name == "Kithling" and gold >= 17:
                                        print("Serah the Sustenance: Ahh yes a Kithling! I favor thee!")
                                        time.sleep(1.3)
                                        print(f"You bought Embergrin Stew with a discounted price of 3 gold! -17 Gold, gold is now {gold} Gold. Max HP is now {max_health} and Max ATK is now {attack_max}.")
                                        player_payment()
                                        time.sleep(1.3)
                                        gold -= 17
                                        max_health += 5
                                        attack_max += 2
                                        break
                                    else:
                                        print(f"You bought Embergrin Stew! -20 Gold, gold is now {gold} Gold. Max HP is now {max_health} and Max ATK is now {attack_max}.")
                                        player_payment()
                                        time.sleep(1.3)
                                        gold -= 20
                                        max_health += 5
                                        attack_max += 2
                                        break
                                # Player chooses "3" and buys Moonpetal Salad
                                elif sanctuary_resto_choice == "3" and gold >= 30:
                                    if race_name == "Kithling" and gold > 25:
                                        print("Serah the Sustenance: Ahh yes a Kithling! I favor thee!")
                                        time.sleep(1.3)
                                        print(f"You bought Moonpetal Salad with a discounted price of 5 gold! -25 Gold, gold is now {gold} Gold. Max HP is now {max_health} and Max ATK is now {attack_max}.")
                                        player_payment()
                                        time.sleep(1.3)
                                        gold -= 25
                                        max_health += 15
                                        break
                                    else:
                                        print(f"You bought Moonpetal Salad! -30 Gold, gold is now {gold} Gold. Max HP is now {max_health} and Max ATK is now {attack_max}.")
                                        player_payment()
                                        time.sleep(1.3)
                                        gold -= 30
                                        max_health += 15
                                        break
                                # Playerr chooses "4" and buys Sunforged Bread
                                elif sanctuary_resto_choice == "4" and gold >= 25:
                                    if race_name == "Kithling":
                                        print("Serah the Sustenance: Ahh yes a Kithling! I favor thee!")
                                        time.sleep(1.3)
                                        print(f"You bought Sunforged Bread with a discounted price of 4 gold! -21 Gold, gold is now {gold} Gold. Max HP is now {max_health} and Max ATK is now {attack_max}.")
                                        player_payment()
                                        time.sleep(1.3)
                                        gold -= 21
                                        max_health += 8
                                        attack_max += 3
                                        break
                                    else:
                                        print(f"You bought Sunforged Bread! -25 Gold, gold is now {gold} Gold. Max HP is now {max_health} and Max ATK is now {attack_max}.")
                                        player_payment()
                                        time.sleep(1.3)
                                        gold -= 25
                                        max_health += 8
                                        attack_max += 3
                                        break
                                # Player chooses "5" and buys Eternal Roast
                                elif sanctuary_resto_choice == "5" and gold >= 40:
                                    if race_name == "Kithling":
                                        print("Serah the Sustenance: Ahh yes a Kithling! I favor thee!")
                                        time.sleep(1.3)
                                        print(f"You bought Eternal Roast with a discounted price of 5 gold! -21 Gold, gold is now {gold} Gold. Max HP is now {max_health} and Max ATK is now {attack_max}.")
                                        player_payment()
                                        time.sleep(1.3)
                                        gold -= 35
                                        max_health += 20
                                        attack_max += 5
                                        break
                                    else:
                                        print(f"You bought Eternal Roast! -40 Gold, gold is now {gold} Gold. Max HP is now {max_health} and Max ATK is now {attack_max}.")
                                        player_payment()
                                        time.sleep(1.3)
                                        gold -= 40
                                        max_health += 20
                                        attack_max += 5
                                        break
                                elif sanctuary_resto_choice == "x":
                                    print("You stepped away from the restaurant...")
                                    time.sleep(1.3)
                                    break
                                else:
                                    print("Invalid choice, try again")
                                    break
                    #
                    elif player_choice_3 == "3":
                        int("Coming soon! You can try Rift of Echoing Souls to test your skills and test out diff classes!")
                    # Player talks to Eternal Inkeeper in eternal Sanctuary
                    elif player_choice_3 == "4":
                        print("You walked towards the Eternal Inkeeper...")
                        time.sleep(1.3)
                        print("Eternal Inkeeper: Ahh yes, traveller, what is it thy want to say to me?")
                        time.sleep(1.3)
                        while True:
                            print(f"What do you want to say?")
                            print("[1]. Know about the history of the Eternal Sanctuary."
                                  "\n[2]. Ask how the Eternal Beings became how they are today."
                                  "\n[3]. Ask about how they get their stocks of food and items in the Eternal Caverns."
                                  "\n[4]. Listen to some gossips going around in the Eternal Village..."
                                  "\n[X]. Exit Menu")
                            player_talk = input("--> ").lower().strip()
                            if player_talk == "1":
                                print(f"{player_name}: 'Greetings, may I ask what is the history if thy Sanctuary if it please thee?'")
                                time.sleep(1.3)
                                eternal_sanctuary_history()
                                time.sleep(1.7)
                                print(f"{player_name} whispers to themselves: 'Hmm interesting...'")
                                time.sleep(1.3)
                            elif player_talk == "2":
                                print(f"{player_name}: 'Ah, if I may, how did you all look like you are right now?'")
                                time.sleep(1.3)
                                eternal_beings_history()
                                time.sleep(1.7)
                            elif player_talk == "3":
                                print(f"{player_name}: 'Thy place is good looking, how to thee get thy stocks and items here?'")
                                time.sleep(1.3)
                                eternal_villagers_survival()
                                time.sleep(1.7)
                            elif player_talk == "4":
                                print(f"{player_name}: 'So Inkeeper, do thee have some... news for me?'")
                                time.sleep(1.3)
                                eternal_inkeeper_gossip()
                                time.sleep(2)
                            elif player_talk == "x":
                                print("You walked away from the Eternal Inkeeper's table.")
                                time.sleep(1.3)
                                break
                            else:
                                print("Invalid Choice, please select an appropriate choice.")
                                continue
                    elif player_choice_3 == "x":
                        soulwarden_farwell()
                        time.sleep(1.3)
                        break
            elif walk_choice_north == "7":
                print("You walk towards the Rift of Echoing Souls — the ground beneath you trembles with memories of countless duels.")
                time.sleep(1.7)
                pygame.mixer.music.fadeout(2000)
                time.sleep(2)
                print("As you approach the arena, a roaring crowd noise greets you...")
                time.sleep(1.3)
                print("Echokeeper: 'Choose thy challenge, and the Rift shall answer.'")
                time.sleep(1.3)
                while True:
                    pygame.mixer.music.load("sounds/rift of echoing souls.ogg")
                    pygame.mixer.music.play(-1)
                    print(f"\n                       --[{player_name}, {race_name} {player_class} | {Fore.RED}{player_health}{Style.RESET_ALL}/{Fore.RED}{max_health}{Style.RESET_ALL} HP | {gold} {Fore.LIGHTYELLOW_EX}Gold{Style.RESET_ALL}]--")
                    print("==================================================================================================================================================================================")
                    print("                                                                                ---[ Rift of Echoing Souls ]---                                                                  ")
                    print(f"<-{Fore.LIGHTGREEN_EX}Tip{Style.RESET_ALL}: {Fore.LIGHTGREEN_EX}Consider checking the enemy info first before you battle. It might help you strategize!{Style.RESET_ALL}")
                    print(f"[1]. Fading Whispers (Difficulty: {Fore.LIGHTGREEN_EX}Easy{Style.RESET_ALL})  [2]. Resounding Cries (Difficulty: {Fore.YELLOW + Style.BRIGHT}Normal{Style.RESET_ALL})")
                    print(f"[3]. Shattered Hymns (Difficulty: {Fore.LIGHTBLACK_EX}Hard{Style.RESET_ALL})  [4]. Eternal Reverberation (Difficulty: {Fore.BLACK}Very Hard{Style.RESET_ALL})")
                    print(f"[5]. Echo of the Ancients (Difficulty: {Fore.RED + Style.BRIGHT}Legendary{Style.RESET_ALL})")
                    print("[i]. Enemy Info.")
                    print("[X]. Leave the Rift of Echoing Souls.")
                    print("==================================================================================================================================================================================")
                    print()
                    arena_choice = input("--> ").lower().strip()
                    if arena_choice == "1":
                        eternal_arena_lvl1()
                        pygame.mixer.music.fadeout(2000)
                        time.sleep(1.3)
                        pygame.mixer.music.load(r"sounds/level 1.ogg")
                        pygame.mixer.music.play(-1)
                        battle(random.choice(["Ashfang_Stalker", "Mirefang_Myconid"]))
                        pygame.mixer.music.fadeout(2000)
                    elif arena_choice == "2":
                        eternal_arena_lvl2()
                        pygame.mixer.music.fadeout(2000)
                        time.sleep(1.3)
                        pygame.mixer.music.load(r"sounds/level 2.ogg")
                        pygame.mixer.music.play(-1)
                        battle(random.choice(["Crystalis_Warden", "Ashveil_Harbringer"]))
                        pygame.mixer.music.fadeout(2000)
                    elif arena_choice == "3":
                        eternal_arena_lvl3()
                        pygame.mixer.music.fadeout(2000)
                        time.sleep(1.3)
                        pygame.mixer.music.load(r"sounds/level 3.ogg")
                        pygame.mixer.music.play(-1)
                        battle(random.choice(["Frostborn_Revenant", "Glacier_Wraith"]))
                        pygame.mixer.music.fadeout(2000)
                        time.sleep(1.3)
                    elif arena_choice == "4":
                        eternal_arena_lvl4()
                        pygame.mixer.music.fadeout(2000)
                        time.sleep(1.3)
                        pygame.mixer.music.load(r"sounds/level 4.ogg")
                        pygame.mixer.music.play(-1)
                        battle(random.choice(["Hollowshade_Sentinel", "Ebonmarrow_Fiend"]))
                        pygame.mixer.music.fadeout(2000)
                    # Player chooses to fight level 5 enemies
                    elif arena_choice == "5":
                        eternal_arena_lvl5()
                        pygame.mixer.music.fadeout(2000)
                        time.sleep(1.3)
                        pygame.mixer.music.load(r"sounds/level 5a.ogg")
                        pygame.mixer.music.play(-1)
                        battle("Emberveil_Serpent")
                        pygame.mixer.music.fadeout(2000)
                        print("Echokeeper: Congratulations, traveller... you defeated the Emberveil Serpent...")
                        time.sleep(1.7)
                        print(f"Echokeeper: Now for the real challenge, I present the {Fore.RED + Style.BRIGHT}VERMILLION TYRANT{Style.RESET_ALL}!!")
                        time.sleep(2.5)
                        pygame.mixer.music.load(r"sounds/level 5.ogg")
                        pygame.mixer.music.play(-1)
                        battle("Vermillion_Tyrant")
                        print("Echokeeper: Well done, traveller. You are now the Conqueror of the Rifts!")
                        pygame.mixer.music.fadeout(2000)
                        time.sleep(1.7)
                    # Enemy infos code
                    elif arena_choice == "i":
                        while True:
                            print("Which level would you want to check the info of?: ")
                            print(f"<- {Fore.LIGHTGREEN_EX}Tip{Style.RESET_ALL}: {Fore.LIGHTGREEN_EX}Each level, you have a random chance of facing one of the enemies{Style.RESET_ALL}.")
                            print("[1]. Level 1   [2]. Level 2")
                            print("[3]. Level 3   [4]. Level 4")
                            print("        [5]. Level 5      ")
                            print("        [X]. Exit menu")
                            arena_info_choice = input("--> ").strip().lower()
                            # Level 1 enemy infos
                            if arena_info_choice == "1":
                                print("                                                             ---{ Level 1 Enemies }--")
                                print("--[ Ashfang Stalker - A predator born of soot and ember, swift and merciless ~ its serrated claws leave wounds that poisons its foes over time. ]--")
                                print("--( HP: 60, Max Attack: 11, Special Ability: Poison )--")
                                print("=" * 65)
                                print("--[ Mirefang Myconid - A lumbering fungus beast from the swamp caverns. Its spores damages foes with great pain. ]--")
                                print("--( HP: 65, Max Attack: 10, Special Ability: None )--")
                                input("\nPress Enter to go back to menu -->  ")
                            # Level 2 enemy infos
                            elif arena_info_choice == "2":
                                print("                                             ---{ Level 2 Enemies }---                                           ")
                                print("--[ Crystalis Warden - A guardian of molten crystal. When its armor cracks, fury consumes it in burning rage. ]--")
                                print("--( HP: 80, Max Attack: 14, Special Ability: None )--")
                                print("=" * 65)
                                print("--[ Ashveil Harbringer - A shrouded herald born from dying embers - every strike leaves trails of burning ash and blood. ]--")
                                print("--( HP: 75, Max Attack 16, Special Ability: Bleed )--")
                                input("\nPress Enter to go back to menu -->  ")
                            # Level 3 enemy infos
                            elif arena_info_choice == "3":
                                print("                                                    --{ Level 3 Enemies }--")
                                print("--[ Frostborn Revenant - Once a knight lost to the tundra's curse, now he wanders - frost and vengeance bound to his soul. ]--")
                                print("--( HP: 90, Max Attack 14, Special Ability: Freeze )--")
                                print("=" * 65)
                                print("--[ Glacier Wraith - A spirit formed of ice and sorrow. It glides without sound, and the air grows still where it passes. ]--")
                                print("--( HP: 95, Max Attack 16, Special Ability: Freeze )--")
                                input("\nPress Enter to go back to menu -->  ")
                            # Level 4 enemy infos
                            elif arena_info_choice == "4":
                                print("                                                     --{ Level 4 Enemies }--")
                                print("--[ Hollowshade Sentinel - Once a guardian of forgotten halls, now a cursed shell - defending shadows that no longer remain. ]--")
                                print("--( HP: 120, Max Attack 18, Special Ability: Bleed )--")
                                print("=" * 65)
                                print("--[ Ebonmarrow Fiend - Born from the bones of the forsaken, its breath drips with venom and decay - a plague given form. ]--")
                                print("--( HP: 130, Max Attack 17, Special ability: Venom )--")
                                input("\nPress Enter to go back to menu -->  ")
                            # Level 5 enemy infos
                            elif arena_info_choice == "5":
                                print("                                                       --{ Level 5 Enemies }--")
                                print("--[ Emberveil Serpent - Forged in molten caverns, this serpent slithers between flame and shadow — its bite burns and bleeds alike. ]--")
                                print("--( HP: 150, Max Attack 20, Special Ability: Bleed )--")
                                print("=" * 65)
                                print("--[ Vermillion Tyrant - Crowned in fire and fury, this ancient beast rules the Rift — each roar ignites the air itself. ]--")
                                print("--( HP: 180, Max attack 22, Special Ability: Rage, the lower its HP, the higher its damgge. )--")
                                input("\nPress Enter to go back to menu -->  ")
                            elif arena_info_choice == "x":
                                print("You close the book of info.")
                                time.sleep(0.5)
                                break
                    elif arena_choice == "x":
                        echokeeper_farewell_lines()
                        time.sleep(1.6)
                        print("So you head out of the Rift of the Echoing Souls...")
                        time.sleep(1)
                        print("The voices of the loud, maddening crowd faints behind you..")
                        pygame.mixer.fadeout(2000)
                        time.sleep(1.2)
                        break
                    else:
                        print("Invalid choice.")
                        break
            elif walk_choice_north == "s":
                print("You walked back south, the smoke and lights of the Stoneheart Armory and Hollow Earth Inn glooms over you...")
                time.sleep(1.5)
                south_eternal_village()
            else:
                pass
        elif move == "4":
            player_eternal_warrior_talking()
chapt5_eternal_village()

