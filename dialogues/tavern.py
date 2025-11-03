import random
#                                         --[CHAPTER 5 TAVERN]--
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