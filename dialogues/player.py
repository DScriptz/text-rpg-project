# Player rests Etenal Sanctuary
import random
def player_sleeping():
    player_sleeps = [
        "You rest within the Eternal Sanctuary, where even time itself seems to sleep. Your wounds fade, and your spirit feels renewed.",
        "The warmth of candlelight and soft hymns cradle your weary soul. You drift into a dreamless rest…",
        "You hand over the coins and settle into your chamber. The Eternal Sanctuary’s tranquil air mends both flesh and spirit.",
        "You rent a room within the Eternal Sanctuary. The silence is deep — the kind that heals.",
        "The chamber hums faintly with the pulse of ancient wards. As you close your eyes, the Sanctuary itself seems to breathe life back into you.",
        "You lie upon sanctified linens woven with threads of moonlight. When you wake, you feel as though touched by the divine."
    ]
    print(random.choice(player_sleeps))
# IRONFANG PLAYER BUY LINES
def shop2_player_buy_ironfang_lines(player_name):
    player_buys_ironfang_lines = [

        f"{player_name}: I shall take this swift blade, master Eternal.\"",
        f"{player_name}: This sword is nimble, I shall wield it well.\"",
        f"{player_name}: By my hand, it shall strike true and fast.\"",
        f"{player_name}: I claim this blade for my travels ahead.\"",
        f"{player_name}: A fine sword! I shall put it to good use.\""
    ]
    print(random.choice(player_buys_ironfang_lines))
# RUNESWORD PLAYER BUY LINES
def shop2_player_buy_runesword_lines(player_name):

    player_buys_runesword_lines = [

        f"{player_name}: These runes call to me, I shall take it.",
        f"{player_name}: I shall wield this ancient sword with honor.",
        f"{player_name}: By its magic, I hope to strike wisely.",
        f"{player_name}: I claim this blade for my quests.",
        f"{player_name}: May this sword guide my hand in battle."
    ]
    print(random.choice(player_buys_runesword_lines))

# HAMMER OF THE DEEP FORGE PLAYER BUY LINES
def shop2_player_buy_hammer_deep_forge_lines(player_name):
    player_buys_hammer_deep_forge_lines = [
        f"{player_name}: This mighty hammer shall be mine.",
        f"{player_name}: I shall crush my foes with this, Eternal.",
        f"{player_name}: By my strength, this hammer shall serve me well.",
        f"{player_name}: I claim this weapon of thunder and stone.",
        f"{player_name}: With this, no armor shall withstand me."
    ]

    print(random.choice(player_buys_hammer_deep_forge_lines))
# BOW WHISPERING PINES PLAYER BUY LINES
def shop2_player_buys_bow_whispering_pines_lines(player_name):
    player_buys_bow_whispering_pines_lines = [

        f"{player_name}: I shall take this bow and let the forest guide me.",
        f"{player_name}: Silent and true, I shall strike unseen.",
        f"{player_name}: By the pines, my aim shall not falter.",
        f"{player_name}: I claim this bow for swift justice.",
        f"{player_name}: My arrows shall fly as whispers through the trees."
    ]
    print(random.choice(player_buys_bow_whispering_pines_lines))
# DAGGER OF THE SHADOWGLASS PLAYER BUY LINES
def shop2_player_buys_dagger_shadowglass_lines(player_name):

    player_buys_dagger_shadowglass_lines = [

        f"{player_name}: I shall wield this dagger from shadow and mist.",
        f"{player_name}: Quick and silent, it shall serve me well.",
        f"{player_name}: By cunning and speed, I shall strike true.",
        f"{player_name}: I claim this blade for secret deeds.",
        f"{player_name}: Shadows shall hide my hand, yet my strike will be deadly."
    ]
    print(random.choice(player_buys_dagger_shadowglass_lines))
# AXE STONEBREAKER PLAYER BUY LINES
def shop2_player_buys_axe_stonebreaker_lines(player_name):
    player_buys_axe_stonebreaker_lines = [

        f"{player_name}: This axe shall rend both stone and foe.",
        f"{player_name}: I claim this mighty weapon for my battles.",
        f"{player_name}: By my strength, none shall stand before me.",
        f"{player_name}: A weapon of power! I shall wield it well.",
        f"{player_name}: Let the stones break beneath its swing."
    ]
    print(random.choice(player_buys_axe_stonebreaker_lines))
# LANCE OF THE ETERNAL GUARD PLAYER BUY LINES
def shop2_player_buys_lance_eternal_lines(player_name):
    player_buys_lance_eternal_lines = [
        f"{player_name}: I shall wield this lance with honor and courage.",
        f"{player_name}: By the Eternal Guard, I claim this weapon.",
        f"{player_name}: Steady and true, it shall guide my hand.",
        f"{player_name}: I shall ride forth with this lance in valor.",
        f"{player_name}: Let this lance serve me in noble deeds."
    ]
    print(random.choice(player_buys_lance_eternal_lines))
# STAFF OF EMBERLIGHT PLAYER BUY LINES
def shop2_player_buys_staff_emberlight_lines(player_name):
    player_buys_staff_emberlight_lines = [

        f"{player_name}: I claim this staff, bearer of ember and flame.",
        f"{player_name}: By its magic, I shall light the darkness.",
        f"{player_name}: I shall wield its fire with wisdom and care.",
        f"{player_name}: Let the ember guide my hand in battle.",
        f"{player_name}: This staff shall serve me well on my quest."

    ]
    print(random.choice(player_buys_staff_emberlight_lines))
# CROSSBOW OF SILENT THUNDER PLAYER BUY LINES
def shop2_player_buys_crossbow_silent_thunder_lines(player_name):
    player_buys_crossbow_silent_thunder_lines = [

        f"{player_name}: I shall take this crossbow, silent as the storm.",
        f"{player_name}: My enemies shall hear naught, yet fall swiftly.",
        f"{player_name}: I claim this weapon to strike from afar.",
        f"{player_name}: Each bolt shall fly true and sure.",
        f"{player_name}: By thunder and silence, I shall prevail."
    ]
    print(random.choice(player_buys_crossbow_silent_thunder_lines))
# WARBLADE OF THE BRAVE PLAYER BUY LINES
def shop2_player_buys_warblade_brave_lines(player_name):
    player_buys_warblade_brave_lines = [
        f"{player_name}: I shall wield this legendary blade with courage.",
        f"{player_name}: May my deeds honor this sword.",
        f"{player_name}: I claim this weapon for battles yet to come.",
        f"{player_name}: With this warblade, I shall carve my name in legend.",
        f"{player_name}: By bravery, I shall master this mighty sword."
    ]
    print(random.choice(player_buys_warblade_brave_lines))