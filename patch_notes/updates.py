
patch_notes = {
    "1.4.2": [
            "Added an inventory system",
            "Polished most of the UI for better immersion & gameplay",
            "Added Rift of Echoing Souls arena",
            "Fixed multiple bugs in battle (especially using potion)"
    ],
    "v1.5.3": [
        "Added Lost Trader mining quest",
        "Added Glowmire Market (unfinished but playable)",
        "Fixed a very weird bug on the Echoing vials shop and Fortune's Toss",
        "Added the missing exit menu feature on Fortune's Toss",
        "Polished the pickaxe menu in Glimmerpick Stall in Glowmire Market",
        "Organized the files for the game"
    ],


}


def show_patch_notes():

    latest_version = list(patch_notes.keys())[-1]

    print("                                                             ----------------------------------------------------------")
    print(f"                                                                               -[PATCH NOTES - {latest_version}]- ")
    print("                                                             ----------------------------------------------------------")
    for note in patch_notes[latest_version]:
        print(f"                                                                - {note}")
    print("                                                             -----------------------------------------------------------")
    print("Press [Enter] to continue")
    input("\n>> ")
