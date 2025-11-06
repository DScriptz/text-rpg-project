# Welcome to my fun first project. Basically it's a combination of my favorite action RPGs (First started Sept 5, 2025)
# First personal project on Python: September update ARPG Alpha. For those who are testing this, this is still in the works so it's not polished yet. Ight thx
# I used AI, online resources and w3schools only for helping me understand each functions and variables and where to put the parameters only. Sep 11, 2025.
# Gameplay is based but not the same to: Dungeons and Dragons, Pokemon, and World of Warcraft (so far)...
# Thank you for playtesting! Hope yall enjoy
# IF YOU'RE PLAYING FOR THE FIRST TIME, I SUGGEST NOT TO SKIP THE DIALOGUE FOR MORE IMMERSION AND STORY CONTEXT
# v.11.5.25 Alpha (Questing and Arena update) updated Nov 5, 2025.
#DefNoInspect
import sys
import os
# import time
# import random
import json
# import pygame
# from colorama import Fore, Style, init
from dialogues import *
from dialogues.player import *
from chapters import *
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
# Load the Class_stats
try:
    with open('class_data.json', 'r') as file:
        class_data = json.load(file)
except FileNotFoundError:
    print("Error: class_data.json is not found! Make sure the file is in the same folder as this script.")

# ============================================
#     GAME FLAGS/STATS AND STARTING DATAA
# ============================================
""" PLAYER DATA """
player_data = {
    "name": "",
    "class": "",
    "race": "",
    "gold": 30,
    "player_health": 0,
    "max_health": 0,
    "attack_max": 0,
    "inventory": {
        "empty bottle": 0,
        "empty vial": 0
    },

}
inventory = player_data["inventory"]
""" LOAD PLAYER DATA"""

# Keywords for dicts
potion_keywords = [
    "potion",
    "draught",
    "elixir",
    "tonic",
    "tea",
    "vial"
]
# player special skill
special_skills = {
    "Warrior": "Power Strike",
    "Rogue": "Shadow Step",
    "Mage": "Ice Shard",
    "Necromancer": "Life Drain",
    "Marksman": "Eagle Eye",
    "Paladin": "Holy Shield",
    "Druid": "Regrowth",
    "Illusionist": "Mirror Image",
    "Alchemist": "Risky Play",
    "Sentinel": "Bulwark Stance",
    "Dev Test": "FAHHHHHHHHHHHHHHH"
}
# Player quest list
player_quests = {}

# Show quest
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
        print(f"- {quest_name} [{Fore.RED + Style.BRIGHT}{status}{Style.RESET_ALL}]")
        if description:
            print(f"   > {description}")
        print()
    input("Press enter to continue:  ")
    play_sound("close quest log", volume=0.8)
# Add quest
def add_quest(quests, name, description):
    if name not in quests:
        quests[name] = {f"status": f"{Fore.RED + Style.BRIGHT}Ongoing{Style.RESET_ALL}", "description": description}
        play_sound("new quest", volume=0.7)
        print(f"\nNew Quest Added: {name}")
        print(f"   > {description}")
    else:
        print(f"\nYou already have the quest: {name}\n")
# Quest gets completed and rewards get to the player
def complete_quest(quests, name):
    global gold, attack_max
    if name in quests:
        quests[name]["status"] = "Completed"
        print(f"\nQuest Completed: {Fore.MAGENTA + Style.BRIGHT}{name}{Style.RESET_ALL}!\n")
        play_sound("quest completed", volume=0.6)
        reward_type = quests[name].get("reward_type")
        reward_value = quests[name].get("reward_value")
        if reward_type == "gold":
            gold += reward_value
            print(f"You received {reward_value} gold! Total Gold: {gold}")
        elif reward_type == "item":
            item_name = reward_value
            if item_name == "Eternal Dagger":
                attack_max += 10
                print(f"You obtained and equipped the {item_name}! (+10 max attack) Max Attack is now {attack_max}")
            else:
                inventory[item_name] = inventory.get(item_name, 0) + 1
                print(f"You received a {item_name}!")
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
        elif trading == "i":
            open_inventory()
        if not trading.isdigit() or int(trading) < 1 or int(trading) > len(echo_vials_trade_items):
            print()
            continue
        index = int(trading)
        item_name = list(echo_vials_trade_items.keys())[index - 1]
        item_price = echo_vials_trade_items[item_name]
        # Check amount the player wants to trade
        try:
            amount = int(input(f"How many {item_name}'s do you want to trade?: "))
            if item_name in player_inventory and player_inventory[item_name] >= amount:
                player_inventory[item_name] -= amount
                gold_earned = amount * item_price
                gold += gold_earned
                print(f"You sold {amount}x {item_name} for {gold_earned} Gold!")
            else:
                print(f"You don't have any {item_name} to trade!")
        except ValueError:
            print("Invalid number.")
            continue
    return player_inventory, gold
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
def random_npc_interaction():
    npc = random.choice(npcs)
    dialogue = random.choice(npc_quest_dialogues)
    print(f"\n{npc['name']}: '{dialogue}'")
    return npc
# Random NPC quests
def offer_random_quest():
    global gold, attack_max
    choose = input("Do you want to accept this quest? (Yes/No): ").strip().lower()
    if choose == "yes":
        npc = random_npc_interaction()
        time.sleep(1.3)
        enemy = random.choice(['Ashfang Stalker', 'Crystalis Warden', 'Glacier Wraith',
                               'Frostborn Revenant', 'Mirefang Myconid', 'Emberveil Serpent'])
        reward_type = random.choice(["Gold", "item"])
        if reward_type == "Gold":
            reward = random.randint(25, 50)
        else:
            reward = random.choice(['Moonfern Tea', 'Healing Potion', 'Greater Healing Potion', 'Eternal Dagger'])
        quest_name = f"Hunt: {enemy}"
        if quest_name in player_quests and player_quests[quest_name]["status"] == "Ongoing":
            print(f"\nYou already have this quest active: {quest_name}")
            return
        quest_description = (f"{npc['name']} seeks your aid in slaying a {enemy} lurking in the Rift of Echoing Souls. "
                             f"Reward: {reward_type}.")
        player_quests[quest_name] = {
            "status": "Ongoing",
            "description": quest_description,
            "reward_type": reward_type,
            "reward_value": reward
        }
        play_sound("new quest", volume=0.7)
        print(f"\nNew Quest Added: {quest_name}")
        print(f"   > {quest_description}")
        time.sleep(1.7)
        print(f"\n{npc['name']}: 'Bring swift end to that creature, traveller. Return when the deed is done.'")
        time.sleep(2)
    else:
        print("You walk away and choose not to help the NPC...")


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
    for item, amount in inventory.items():
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
    "Ashfang Carpace": 5,
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
        remaining = inventory.get("empty bottle, 0")
        if inventory.get("empty bottle", 0) > 0:
            inventory["empty bottle"] -= 1
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
            player_health += 10
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
    """ PLAYS THE BACKGROUND MUSIC FOR THE STONEHEART ARMORY """
    play_music("stoneheart armory", volume=1, loop=True)
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
                """ STONEHEART ARMORER NPC VOICE """
                play_sound("stoneheart_armory_npc", volume=0.9)
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
                        shop2_player_buy_ironfang_lines(player_name)
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
                        shop2_player_buy_runesword_lines(player_name)
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
                        shop2_player_buy_hammer_deep_forge_lines(player_name)
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
                        shop2_player_buys_bow_whispering_pines_lines(player_name)
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
                        shop2_player_buys_dagger_shadowglass_lines(player_name)
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
                        shop2_player_buys_axe_stonebreaker_lines(player_name)
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
                        shop2_player_buys_lance_eternal_lines(player_name)
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
                        shop2_player_buys_staff_emberlight_lines(player_name)
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
                        shop2_player_buys_crossbow_silent_thunder_lines(player_name)
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
                        shop2_player_buys_warblade_brave_lines(player_name)
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
# Fortune's toss code
def play_fortune_toss(gold):
    print("\nElara Wraithand: Now tell me stranger, what side of the coin will you bet on tonight?")
    time.sleep(1.3)
    while True:
        print("==========================================================================================================================================================================================")
        print("                                                                                         -{ Fortune's Toss }-")
        print(f"                                                                                    -[{player_name} | {Fore.RED}{player_health}{Style.RESET_ALL}/{Fore.RED}{max_health}{Style.RESET_ALL} | {gold} {Fore.LIGHTYELLOW_EX}Gold{Style.RESET_ALL}]-")
        print("\n                                                                                        [H] Heads | [T] Tails.")
        print("                                                                                            [X] Exit Menu.")
        print("==========================================================================================================================================================================================")

        game_choice = input("\n>> ").lower().strip()
        coin_choice = None
        match game_choice:
            case "h":
                coin_choice = "heads"
            case "t":
                coin_choice = "tails"
            case "x":
                print("You walked away from the table..")
                break
            case _:
                print("Not a valid choice.")
                continue
        # Ask for bet amount
        try:
            bet_amount = int(input("Enter bet amount: ").strip())
        except ValueError:
            print("That's not a number! The coin refuses your confusion.")
            continue

        if bet_amount <= 0 or bet_amount < 10:
            print("You must bet at least 10 gold!!!")
            continue
        if bet_amount > gold:
            print("Elena Wraithand: Hold thy horses there stranger, you don't have enough gold.")
            continue
        # toss outcome
        toss = random.choice(["heads", "tails"])

        print(f"\nElena Wraithand flips the coin...")
        play_sound("coin flip", volume=1)
        time.sleep(2)
        print(f"\nIt lands on {toss.upper()}!")
        play_sound("coin drop", volume=0.8)
        time.sleep(2)
        # Player wins or losses
        match(coin_choice == toss):
            case True:
                gold += bet_amount * 2
                player_wins_fortune_toss()
                print(f"\nYou won double the amount of your bet amount! + {bet_amount}!")
                time.sleep(1.85)
            case False:
                gold -= bet_amount
                player_losses_fortune_toss()
                time.sleep(1.85)
                print(f"\nYou lost {bet_amount} gold...")
                time.sleep(1.5)
        return gold
# Game title & music--------------------------------------------------------------------------------------------------------------------------------------#
pygame.mixer.music.load(land_of_bravery_bgm)
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)
print("                                                                             ------------------------------------")
print(Style.BRIGHT + Fore.LIGHTMAGENTA_EX + "                                                                             === Quest of the Eternal Caverns ===")
print(f"{Style.BRIGHT + Fore.LIGHTRED_EX}                                                                                    -[ Developer Build ]-{Style.RESET_ALL}")
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
player_data["name"] = input("\nOld Man: What is thy name, traveller?: ").strip()
while player_data["name"] == "":
    print("Old Man: I know you have the ability speak, traveller.")
    player_data["name"] = input("\nOld Man: What is thy name, traveller? ").strip()

player_name = player_data["name"]

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
time.sleep(1.4)
add_quest(player_quests, "Forging a hero...", "Pick a class and a race.")
time.sleep(1.3)
def class_choosing(player_data):
    print("\nLance the Grandmaster: Very well, now what class do you choose?")
    time.sleep(1.5)
    print("\nChoose thy Class: ")
    time.sleep(1.5)
    # Class list
    print()
    print("=======================================================================================================")
    print("                                          -CLASS LIST-                                                   ")
    print("=======================================================================================================")
    print(
        f"(<{Fore.LIGHTGREEN_EX + Style.BRIGHT}Tip: Every class is unique, fun and balanced! Pick what you will enjoy and have fun!{Style.RESET_ALL}>)")
    print()
    # Warrior Description
    print(f"{Fore.YELLOW}\n1. Warrior{Style.RESET_ALL} – A hardened fighter with unmatched strength and resilience.")
    print("[Base Health: 75 | Base Attack: 8]")
    print("Special Skill: [Power Strike] - Unleash raw might to deliver a crushing blow that shatters defenses!")
    # Rogue Description
    print(f"{Fore.BLUE}\n2. Rogue{Style.RESET_ALL} – A swift shadow who strikes fast and critical.")
    print("[Base Health: 50 | Base Attack: 9]")
    print("Special Skill: [Shadow Step] - Vanish into darkness, striking swiftly and evading the next attack.")
    # Mage Description
    print(
        f"{Fore.LIGHTMAGENTA_EX + Style.BRIGHT}\n3. Mage{Style.RESET_ALL} – A frail but strong wielder of a devastating arcane power.")
    print("[Base Health: 60 | Base Attack: 12]")
    print("Special Skill: [Ice Shard] - Vanish into darkness, striking swiftly and evading the next attack.")
    # Necromancer Description
    print(f"{Fore.LIGHTRED_EX + Style.DIM}\n4. Necromancer{Style.RESET_ALL} – A dark conjurer who commands the dead.")
    print("[Base Health: 55 | Base Attack: 9]")
    print("Special Skill: [Life Drain] - Sap the life (+3 Heal) from your enemy, wounding them as your own strength returns.")
    print("Passive Skill: [Summon Undead] - Call upon forbidden rites to raise a fallen soul, binding it to your will to fight once more.")
    # Marksman Description
    print(
        f"{Fore.LIGHTCYAN_EX + Style.DIM}\n5. Marksman{Style.RESET_ALL} – A precise hunter who slays from afar with deadly accuracy.")
    print("[Base Health: 56 | Base Attack: 10]")
    print(
        "Special Skill: [Eagle Eye] - Focus with deadly precision — your next attack will have a guaranteed critical chance!")
    # Paladin Description
    print(
        f"{Fore.LIGHTYELLOW_EX + Style.BRIGHT}\n6. Paladin{Style.RESET_ALL} – A holy knight who balances might with divine protection.")
    print("[Base Health: 65 | Base Attack: 8]")
    print("Special Skill: [Holy Shield] - Raise a divine barrier that blocks the next incoming strike.")
    print("Passive Skill: [Holy Aura] - Call upon the Spirit and heal yourself for 3-5 HP upon defending")
    # Druid Description
    print(
        f"{Fore.GREEN + Style.BRIGHT}\n7. Druid{Style.RESET_ALL} – A nature sage who heals allies and bends the wilds.")
    print("[Base Health: 60 | Base Attack: 11]")
    print("Special Skill: [Regrowth] - Call upon nature’s essence (Heals 3-5 HP) to restore your vitality mid-battle.")
    # Illusionist Description
    print(
        f"{Fore.LIGHTBLACK_EX + Style.DIM}\n8. Illusionist{Style.RESET_ALL} – A trickster who deceives foes and slips past danger.")
    print("[Base Health: 57 | Base Attack: 10]")
    print(
        "Special Skill: [Mirror Image] - Create phantom doubles to confuse your foe to hit themselves and evade their blows.")
    # Alchemist Description
    print(
        f"{Fore.RED + Style.BRIGHT}\n9. Alchemist{Style.RESET_ALL} – A daring experimenter wielding volatile potions.")
    print("[Base Health: 58 | Base Attack: 13]")
    print(
        "Special Skill: [Risky Play] - Gamble your safety for volatile power — throw your concoction & deal great damage or suffer the backlash.")
    # Sentinel Description
    print(
        f"{Fore.CYAN + Style.BRIGHT}\n10. Sentinel{Style.RESET_ALL} – A living bulwark, nearly unbreakable in defense.")
    print("[Base Health: 80 | Base Attack: 7]")
    print(
        "Special Skill: [Bulwark Stance] - Fortify your body into living stone, reducing enemy damage but dulling your strikes.")
    print("Passive Skill: [War Cry] - Cry for battle, increasing your attack!")
    # Quit choiceeee
    print("\nQ. Quit")
    # Choice logic
    choice = input("\nEnter 1-10 or 'q' to quit: ")
    match choice:
        case "q":
            print("Only such coward back off at the height of pressure, BE GONE!")
            sys.exit()
    if choice in class_data:
        chosen_class = class_data[choice]

        player_data["class"] = chosen_class["name"]
        player_data["attack_max"] = chosen_class["attack"]
        player_data["player_health"] = chosen_class["health"]
        player_data["max_health"] = chosen_class["health"]

        print(f"\nLance the Grandmaster: Ahh yes a {player_data['class']} lets see how far you'll go.")

        print(f"\n{player_data['name']}:")
        print(f"Health: {player_data['player_health']} | {player_data['max_health']},")
        print(f"Attack: {player_data['attack_max']}")
        print(f"Gold: {player_data['gold']}")
    else:
        print("Oh a nameless villagerr")
        player_data["class"] = "Villager"
        player_data["player_health"] = 30
        player_data["max_health"] = 30
        player_data["attack_max"] = 5
    return player_data

# Player data
player_data = class_choosing(player_data)
player_class = player_data["class"]
player_health = player_data["player_health"]
max_health = player_data["max_health"]
attack_max = player_data["attack_max"]
gold = player_data["gold"]
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
def race_choosing(player_data):
    # PLayer Chooses race:
    print(f"Lance, the Grandmaster: 'Wise choice {player_data["name"]}, Now If I may ask, what is thy race?'")
    time.sleep(1)
    print("Choose your Race:")
    print()
    print("=======================================================================================================")
    print("                                           --RACE LIST--                                                   ")
    print(
        f"\n(<{Fore.LIGHTGREEN_EX + Style.BRIGHT}Tip: Some races have discounts on certain shops, choose what you'll enjoy and have fun!{Style.RESET_ALL}>)")
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
    match chosen_race:
        case "1":
            player_data["race"] = "Human"
            player_data["player_health"] += 1
            player_data["max_health"] += 1
            player_data["attack_max"] += 1
        case "2":
            player_data["race"] = "Sylvari"
            player_data["player_health"] -= 4
            player_data["max_health"] -= 4
            player_data["attack_max"] += 2
        case "3":
            player_data["race"] = "Gorvak"
            player_data["player_health"] +=  12
            player_data["max_health"] += 12
            player_data["attack_max"] -= 1
        case "4":
            player_data["race"] = "Wraithkin"
            player_data["player_health"] -= 8
            player_data["max_health"] -= 8
            player_data["attack_max"] += 4
        case "5":
            player_data["race"] = "Solarian"
            player_data["player_health"] += 6
            player_data["max_health"] += 6
            player_data["attack_max"] += 1
        case "6":
            player_data["race"] = "Stoneborn"
            player_data["player_health"] += 10
            player_data["max_health"] += 10
        case "7":
            player_data["race"] = "Kithling"
            player_data["player_health"] -= 3
            player_data["max_health"] -= 3
            player_data["attack_max"] += 1
        case "8":
            player_data["race"] = "Infernal"
            player_data["player_health"] -= 6
            player_data["max_health"] -= 6
            player_data["attack_max"] += 2
        case "9":
            player_data["race"] = "Drakonid"
            player_data["player_health"] += 11
            player_data["max_health"] += 11
            player_data["attack_max"] += 2
        case "10":
            player_data["race"] = "Lunari"
            player_data["player_health"] -= 7
            player_data["max_health"] -= 7
            player_data["attack_max"] += 3
        case _:
            print("Unknown choice. Defaulting to Human.")
            player_data["race"] = "Human"
            player_data["max_health"] += 1
            player_data["player_health"] += 1
            player_data["attack_max"] += 1

    print(f"\n{player_data['name']}, your stats are now,")
    print(f"Race: {player_data['race']},")
    print(f"Class: {player_data['class']},")
    print(f"Health: {player_data['player_health']} | {player_data['max_health']},")
    print(f"Attack: {player_data['attack_max']}")
    print(f"Gold: {player_data['gold']}")

    return player_data
# Player gets the race benefits
# After race selection
player_data = race_choosing(player_data)
race_name = player_data["race"]
player_health = player_data["player_health"]
max_health = player_data["max_health"]
attack_max = player_data["attack_max"]
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
print(f"                                                       -SHOPKEEPER ITEMS-                                                               ")
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
"""
THIS HANDLES THE GAME'S BATTLES
"""
# noinspection PyUnusedLocal
def battle(enemy_key):
    global player_health, max_health, player_class, attack_max
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
                print(f"{Fore.LIGHTGREEN_EX}[S]. Special Skill: {special_skills.get(player_class, 'Special Skill')}{Style.RESET_ALL}")
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
                        inventory["empty bottle"] += 1
                        # Getting potion data
                        data = potion_data.get(potion_key, {})
                        heal = data.get("heal", 0)
                        effect = data.get("effect")
                        value = data.get("value")
                        duration = data.get("duration", 0)
                        player_health = min(max_health, player_health + heal)
                        print(f"You drink a {potion_key.title()} and restore {heal} HP. ({potion_list[potion_key]} left!)")
                        play_sound("drink potion", volume=1)
                        print(f"Empty bottles: {inventory['empty bottle']}.")
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
                    time.sleep(1.3)
                    gold = max(0, gold -20)
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
                continue
            # Player using special skill
            elif action.lower() == "s" and skill_cooldown_timer == 0:
                print(f"\nYou unleash {special_skills.get(player_class, 'Special Skill')}!!")
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
                    print(f"{special_skills.get(player_class, 'Special Skill')} is ready!")
                    time.sleep(1)
                else:
                    print(f"{special_skills.get(player_class, 'Special Skill')} on COOLDOWN!")
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
                    inventory[dropped_items] = inventory.get(dropped_items, 0) + 1
                    print(f"The {enemy_name} dropped a {dropped_items}")
                for quest_name, quest_data in player_quests.items():
                    if quest_data["status"] == "Ongoing" and enemy_name in quest_name:
                        complete_quest(player_quests, quest_name)
                        time.sleep(1.3)
                break

# Before going to the caverns narrative
pygame.mixer.music.load(land_of_bravery_bgm)
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)
# CHapter 2
add_quest(player_quests, "First big step!", "Head down to the Eternal Caverns and conquer what's coming...")
player_name = chapt2_eternal_caverns(player_name, race_name, player_class,player_health, max_health, gold)
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
        south_eternal_village(player_data, inventory)
    else:
        print("You skipped the Dialogue!")
        pygame.mixer.music.fadeout(2000)
        south_eternal_village(player_data, inventory)

    # Start of the Chapter 5 Eternal village adventure
def south_eternal_village(player_data, inventory):
    global player_name, player_class, race_name, player_health, max_health, attack_max, gold
    global hearthfire_stock, mead_stock, spirits_stock, hp_change
    while True:
        pygame.mixer.music.load(r"sounds/Eternal Village bg.ogg")
        pygame.mixer.music.play(-1)
        print()
        print(f"\n                        --[{player_data["name"]}, {race_name} {player_class} | {Fore.RED}{player_health}{Style.RESET_ALL}/{Fore.RED}{max_health}{Style.RESET_ALL} HP | {gold} {Fore.LIGHTYELLOW_EX}Gold{Style.RESET_ALL}]--")
        if random.random() < 0.3:
            print("\nAs you wander through the glowing streets, a voice calls out to you...")
            time.sleep(1.3)
            offer_random_quest()
        else:
            print()
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
                    print("You step out of the Hollow Earth Inn, the smell of roasted meat and smoke fading behind you as the village square spreads ahead...")
                    time.sleep(2)
                    player_data, inventory = south_eternal_village(player_data, inventory)
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
            player_data, inventory = south_eternal_village(player_data, inventory)
        # Player chooses to go North (3. North)
        elif move == "3":
            print(
                "You head North, where the towering Hall of the Everlight glows like a beacon, the Spindle of Tales hums with forgotten stories,"
                " and the Echoing Vilas Apothecary breathes a scent of strange potions through the cool cavern air.")
            time.sleep(2)
            if random.random() < 0.3:
                print("\nAs you wander through the glowing streets, a voice calls out to you...")
                time.sleep(1.3)
                offer_random_quest()
            else:
                print()
            print(f"\n                                  --[{player_data["name"]}, {race_name} {player_class} | {Fore.RED}{player_health}{Style.RESET_ALL}/{Fore.RED}{max_health}{Style.RESET_ALL} HP | {gold} {Fore.LIGHTYELLOW_EX}Gold{Style.RESET_ALL}]--")
            time.sleep(1)
            print("Where do you want to go?"
                  "\n[1]. Walk to the Spindle of Tales."
                  "\n[2]. Venture through the Hall of the Everlight. (Coming soon)"
                  "\n[3]. Go to the Echoing Vials - Potion Shop."
                  "\n[4]. Explore deeper in the Eternal Caverns. (Coming soon)"
                  "\n[5]. Check out the Glowmire Market. (Coming soon)" ### DO TOMORROW OR THIS WEEK ###
                  "\n[6]. Visit the Eternal Sanctuary."
                  "\n[7]. Compete in the Rift of Echoing Souls."  
                  "\n[S]. Go back.")
            walk_choice_north = input("> ")
            # Player chooses where to go
            if walk_choice_north == "1":
                if random.random() < 0.3:
                    print("\nAs you wander through the glowing streets, a voice calls out to you...")
                    time.sleep(1.3)
                    offer_random_quest()
                else:
                    print()
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
                                print(f"{player_name}: 'I humbly accept, dear Loreweaver.'")
                                time.sleep(1.3)
                                add_quest(player_quests, "The answers lies in the scroll.", "Find an Emberleaf Blossom deeper onto the cave...")
                                time.sleep(1.3)
                                break
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
                        thread_of_fate(player_name)
                        time.sleep(2)
                    # Player leaves Spindle of Tales
                    elif player_choice_2 == "4":
                        loreweaver_farewell_lines()
                        time.sleep(2)
                        print(
                            "You step out of the Spindle of Tales, and the familiar streets of the Eternal Cavern Village stretch before you,"
                            " bathed in the soft glow of lanterns that dance like distant stars.")
                        time.sleep(2)
                        player_data, inventory = south_eternal_village(player_data, inventory)
            elif walk_choice_north == "2":
                print("Coming soon... Chapter 6: Truth unveiled")
                time.sleep(1.3)
                print("Thanks for giving my game a chance, You can still try the other features.")
            elif walk_choice_north == "3":
                if random.random() < 0.3:
                    print("\nAs you wander through the glowing streets, a voice calls out to you...")
                    time.sleep(1.3)
                    offer_random_quest()
                else:
                    print()
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
                        inventory, gold = echo_vials_trade(inventory, gold)
                    # Player opens the inventory
                    elif player_choice_1 == "4":
                        print("You open your Inventory...")
                        time.sleep(1.3)
                        open_inventory()
                    elif player_choice_1 == "x":
                        print("You walk out of the Echoing Vials, the bubbling of the potions are heard fainting behind you...")
                        pygame.mixer.music.fadeout(2000)
                        player_data, inventory = south_eternal_village(player_data, inventory)
            elif walk_choice_north == "4":
                print("Coming soon! You can try Rift of Echoing Souls to test your skills and test out diff classes!")
                time.sleep(1.3)
            elif walk_choice_north == "5":
                print("Coming soon! You can try Rift of Echoing Souls to test your skills and test out diff classes!")
            elif walk_choice_north == "6":
                if random.random() < 0.3:
                    print("\nAs you wander through the glowing streets, a voice calls out to you...")
                    time.sleep(1.3)
                    offer_random_quest()
                else:
                    print()
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
                    print(f"                                 -[{player_name}: {race_name} {player_class} | {Fore.RED}{player_health}{Style.RESET_ALL}/{Fore.RED}{max_health}{Style.RESET_ALL} | {gold} {Fore.LIGHTYELLOW_EX}Gold{Style.RESET_ALL}]-")
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
                    # Player walks towards the Eternal Sanctuary restaurant
                    elif player_choice_3 == "2":
                        print("You walked towards the tasty and soothing smell of the food...")
                        time.sleep(1.3)
                        serah_line()
                        time.sleep(1.3)
                        # Show the menu to the player
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
                        """Choice given for the player when they go to the Restaurant"""

                        while True:
                            sanctuary_resto_choice = input("\n--> ").lower().strip()
                            if sanctuary_resto_choice == "x":
                                print("You stepped away from the restaurant...")
                                time.sleep(1.3)
                                break

                            elif sanctuary_resto_choice == "1" and gold >= 15:
                                if race_name == "Kithling" and gold >= 12:
                                    print("Serah the Sustenance: Ahh yes a Kithling! I favor thee!")
                                    time.sleep(1.3)
                                    print(f"You bought Celestial Broth with a discounted price of 3 Gold! -12 Gold, Max HP is now {max_health}.")
                                    player_payment()
                                    time.sleep(1.3)
                                    gold -= 12
                                    max_health += 10
                                    break
                                else:
                                    gold -= 15
                                    max_health += 10
                                    print(f"You bought Celestial Broth! -15 Gold, Max HP is now {max_health}")
                                    player_payment()
                                    time.sleep(1.3)
                                    break

                            elif sanctuary_resto_choice == "2" and gold >= 20:
                                if race_name == "Kithling" and gold >= 17:
                                    print("Serah the Sustenance: Ahh yes a Kithling! I favor thee!")
                                    time.sleep(1.3)
                                    print(f"You bought Embergrin Stew with a discounted price of 3 gold! -17 Gold, Max HP is now {max_health} and Max ATK is now {attack_max}.")
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

                            elif sanctuary_resto_choice == "3" and gold >= 30:
                                if race_name == "Kithling" and gold > 25:
                                    print("Serah the Sustenance: Ahh yes a Kithling! I favor thee!")
                                    time.sleep(1.3)
                                    print(f"You bought Moonpetal Salad with a discounted price of 5 gold! -25 Gold, Max HP is now {max_health} and Max ATK is now {attack_max}.")
                                    player_payment()
                                    time.sleep(1.3)
                                    gold -= 25
                                    max_health += 15
                                    break
                                else:
                                    print(f"You bought Moonpetal Salad! -30 Gold, Max HP is now {max_health} and Max ATK is now {attack_max}.")
                                    player_payment()
                                    time.sleep(1.3)
                                    gold -= 30
                                    max_health += 15
                                    break

                            elif sanctuary_resto_choice == "4" and gold >= 25:
                                if race_name == "Kithling":
                                    print("Serah the Sustenance: Ahh yes a Kithling! I favor thee!")
                                    time.sleep(1.3)
                                    print(f"You bought Sunforged Bread with a discounted price of 4 gold! -21 Gold, Max HP is now {max_health} and Max ATK is now {attack_max}.")
                                    player_payment()
                                    time.sleep(1.3)
                                    gold -= 21
                                    max_health += 8
                                    attack_max += 3
                                    break
                                else:
                                    print(f"You bought Sunforged Bread! -25 Gold, Max HP is now {max_health} and Max ATK is now {attack_max}.")
                                    player_payment()
                                    time.sleep(1.3)
                                    gold -= 25
                                    max_health += 8
                                    attack_max += 3
                                    break

                            elif sanctuary_resto_choice == "5" and gold >= 40:
                                if race_name == "Kithling":
                                    print("Serah the Sustenance: Ahh yes a Kithling! I favor thee!")
                                    time.sleep(1.3)
                                    print(f"You bought Eternal Roast with a discounted price of 5 gold! -21 Gold, Max HP is now {max_health} and Max ATK is now {attack_max}.")
                                    player_payment()
                                    time.sleep(1.3)
                                    gold -= 35
                                    max_health += 20
                                    attack_max += 5
                                    break
                                else:
                                    print(f"You bought Eternal Roast! -40 Gold, Max HP is now {max_health} and Max ATK is now {attack_max}.")
                                    player_payment()
                                    time.sleep(1.3)
                                    gold -= 40
                                    max_health += 20
                                    attack_max += 5
                                    break
                            else:
                                print("Invalid choice, try again")
                                break
                    # player plays Fortune's Toss
                    elif player_choice_3 == "3":
                        print("\nYou walk towards the busy table...")
                        time.sleep(1.3)
                        print("\nAs you approach, you see people on this table handing out gold, some are losing it, some are winning...")
                        time.sleep(1.7)
                        elara_wraithand_dialogue()
                        time.sleep(1.75)
                        gold = play_fortune_toss(gold)
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
                        soulwarden_farwell(player_name)
                        time.sleep(1.3)
                        player_data, inventory = south_eternal_village(player_data, inventory)
            elif walk_choice_north == "7":
                if random.random() < 0.3:
                    print("\nAs you wander through the glowing streets, a voice calls out to you...")
                    time.sleep(1.3)
                    offer_random_quest()
                else:
                    print()
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
                    print("[Q]. Quest List")
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
                        player_data, inventory = south_eternal_village(player_data, inventory)
                    elif arena_choice == "q":
                        show_quest_log(player_quests)
                        continue
                    else:
                        print("Invalid choice.")
                        break
            elif walk_choice_north == "s":
                print("You walked back south, the smoke and lights of the Stoneheart Armory and Hollow Earth Inn glooms over you...")
                time.sleep(1.5)
                player_data, inventory = south_eternal_village(player_data, inventory)
            else:
                pass
        elif move == "4":
            player_eternal_warrior_talking()
        return player_data
chapt5_eternal_village()



