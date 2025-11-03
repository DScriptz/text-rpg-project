# Elara Wraithand (eternal sanctuary: Fortune's Toss) lines
import random
elara_wraithand_lines = [
    "Elara Wraithand: Ah… Fortune awaits, traveler. Shall we see if she graces your hand tonight?",
    "Elara Wraithand: Heads or tails — such a tiny choice to tempt such vast fate.",
    "Elara Wraithand: Your gold glimmers beautifully. Let’s see if luck finds it worthy.",
    "Elara Wraithand: I’ve watched empires crumble to a coin’s whim. Care to tempt yours?",
    "Elara Wraithand: No spells, no deceit — only the whisper of destiny as it spins.",
    "Elara Wraithand: Watch closely… in this moment, even fortune forgets who she favors."
]
def elara_wraithand_dialogue():
    print(random.choice(elara_wraithand_lines))
# Player wins in fortune's toss
elena_wraithand_win_lines = [
    "Elara Wraithand: Fortune smiles — and it seems she rather likes your company tonight.",
    "Elara Wraithand: A perfect flip… the coin bows to your will.",
    "Elara Wraithand: Luck dances with you, traveler. Don’t let her slip away so soon.",
    "Elara Wraithand: Gold finds its way to those who listen to destiny’s whisper.",
    "Elara Wraithand: Even fate applauds your boldness. Well played.",
    "Elara Wraithand: The coin spins true, and your courage is rewarded in kind."
]
def player_wins_fortune_toss():
    print(random.choice(elena_wraithand_win_lines))
# Player losses in fortune's toss
elena_wraithand_lost_lines = [
    "Elara Wraithand: Ah… fortune turns her face away. She can be quite the fickle muse.",
    "Elara Wraithand: The coin laughs softly — seems it favors me this round.",
    "Elara Wraithand: Don’t pout, traveler. Even loss has its own strange charm.",
    "Elara Wraithand: Fate’s a cruel flirt, isn’t she? Always leaving hearts — and purses — wanting.",
    "Elara Wraithand: Gold departs as easily as breath… but both return, in time.",
    "Elara Wraithand: The coin falls cold. Perhaps next toss, it will remember your name."
]
def player_losses_fortune_toss():
    print(random.choice(elena_wraithand_lost_lines))