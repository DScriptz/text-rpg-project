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
#-----------------------------------------------------------------------------------------------------------#
#                                                CHAPTER 5
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