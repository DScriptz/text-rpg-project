import time
from colorama import Fore, Style, init
init(autoreset=True)
import pygame

# -Chapter 2-
def chapt2_eternal_caverns(player_name, race_name, player_class,
                           player_health, max_health, gold):
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
    return player_name